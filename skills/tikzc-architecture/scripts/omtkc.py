# /// script
# requires-python = ">=3.10"
# dependencies = ["pyyaml>=6"]
# ///
"""Checks and bookkeeping for .omtkc/ architecture documentation.

Usage (from any directory; `python3 scripts/omtkc.py ...` also works without uv):
    uv run scripts/omtkc.py check [OMTKC_DIR]   structural validation; exit 1 on errors
    uv run scripts/omtkc.py tree  [OMTKC_DIR]   element hierarchy and validation state
    uv run scripts/omtkc.py stale [OMTKC_DIR]   elements whose sources changed since analysis
    uv run scripts/omtkc.py stamp GROUP_DIR --check pass|fail --visual inspected|pending
                                            record the render block in GROUP_DIR/meta.yaml
    uv run scripts/omtkc.py hash  FILE...     sha256 of files

Only `stamp` writes; every other command is read-only.

OMTKC_DIR defaults to ./.omtkc. The format is described in references/format.md.
PyYAML is used when installed; otherwise a built-in parser reads the YAML subset
described there and rejects anything outside it.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path

try:
    import yaml
except ImportError:  # fall back to parse_yaml_subset below
    yaml = None

SCHEMA = "omtkc/1"
KINDS = {"group", "leaf"}
STATUSES = {"active", "retired"}
CHECK_STATES = {"pass", "fail"}
VISUAL_STATES = {"inspected", "pending"}
ID_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
LINK_PATTERN = re.compile(r"!?\[[^\]]*\]\(\s*<?([^)\s>]+)>?(?:\s+\"[^\"]*\")?\s*\)")


@dataclass
class Element:
    path: str  # relative to the .omtkc directory, e.g. "data-flow/renderer"
    directory: Path
    meta: dict = field(default_factory=dict)

    @property
    def kind(self) -> str:
        return self.meta.get("kind", "")

    @property
    def status(self) -> str:
        return self.meta.get("status", "active")


@dataclass
class Report:
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    def error(self, where: str, message: str) -> None:
        self.errors.append(f"ERROR {where}: {message}")

    def warn(self, where: str, message: str) -> None:
        self.warnings.append(f"WARN  {where}: {message}")


# --- YAML --------------------------------------------------------------------
# Without PyYAML, read the subset that config.yaml and meta.yaml use: nested
# mappings with plain keys, block and flow lists of scalars, and plain or quoted
# scalars. Anything else is an error rather than a guess.


class YAMLSubsetError(ValueError):
    pass


YAML_ERRORS = (YAMLSubsetError,) if yaml is None else (yaml.YAMLError,)
YAML_KEY = re.compile(r"^([A-Za-z0-9_][\w.-]*)\s*:(?:\s+(.*))?$")
YAML_INT = re.compile(r"^[-+]?(?:0|[1-9][0-9]*)$")
YAML_NULL = {"", "~", "null", "Null", "NULL"}
YAML_BOOL = {
    **dict.fromkeys(("true", "True", "TRUE", "yes", "Yes", "YES", "on", "On", "ON"), True),
    **dict.fromkeys(("false", "False", "FALSE", "no", "No", "NO", "off", "Off", "OFF"), False),
}


def parse_yaml(text: str):
    return yaml.safe_load(text) if yaml is not None else parse_yaml_subset(text)


def parse_yaml_subset(text: str):
    lines: list[tuple[int, int, str]] = []  # (line number, indent, content)
    for number, raw in enumerate(text.splitlines(), 1):
        content = strip_yaml_comment(raw).rstrip()
        if not content.strip():
            continue
        indent = len(content) - len(content.lstrip(" "))
        if content[indent] == "\t":
            raise YAMLSubsetError(f"line {number}: tab indentation")
        if content.strip() in ("---", "..."):
            raise YAMLSubsetError(f"line {number}: document markers are not supported without PyYAML")
        lines.append((number, indent, content.strip()))
    if not lines:
        return None
    value, i = parse_yaml_block(lines, 0, lines[0][1])
    if i < len(lines):
        raise YAMLSubsetError(f"line {lines[i][0]}: unexpected indentation")
    return value


def strip_yaml_comment(line: str) -> str:
    quote = None
    for i, ch in enumerate(line):
        if quote:
            if ch == quote:
                quote = None
        elif ch in "'\"" and (i == 0 or line[:i].rstrip()[-1:] in ("", ":", "-", "[", ",")):
            quote = ch
        elif ch == "#" and (i == 0 or line[i - 1].isspace()):
            return line[:i]
    return line


def is_yaml_item(content: str) -> bool:
    return content == "-" or content.startswith("- ")


def parse_yaml_block(lines: list[tuple[int, int, str]], i: int, indent: int):
    if is_yaml_item(lines[i][2]):
        return parse_yaml_list(lines, i, indent)
    result: dict = {}
    while i < len(lines) and lines[i][1] == indent:
        number, _, content = lines[i]
        match = YAML_KEY.match(content)
        if not match:
            raise YAMLSubsetError(f"line {number}: expected 'key: value', got '{content}'")
        key, rest = match.group(1), (match.group(2) or "").strip()
        i += 1
        if rest:
            result[key] = parse_yaml_scalar(rest, number)
        elif i < len(lines) and lines[i][1] > indent:
            result[key], i = parse_yaml_block(lines, i, lines[i][1])
        elif i < len(lines) and lines[i][1] == indent and is_yaml_item(lines[i][2]):
            result[key], i = parse_yaml_list(lines, i, indent)
        else:
            result[key] = None
    if i < len(lines) and lines[i][1] > indent:
        raise YAMLSubsetError(f"line {lines[i][0]}: unexpected indentation")
    return result, i


def parse_yaml_list(lines: list[tuple[int, int, str]], i: int, indent: int):
    items = []
    while i < len(lines) and lines[i][1] == indent and is_yaml_item(lines[i][2]):
        number, _, content = lines[i]
        item = content[1:].strip()
        if not item or YAML_KEY.match(item) or (i + 1 < len(lines) and lines[i + 1][1] > indent):
            raise YAMLSubsetError(f"line {number}: only scalar list items are supported without PyYAML")
        items.append(parse_yaml_scalar(item, number))
        i += 1
    return items, i


def parse_yaml_scalar(text: str, number: int, in_flow: bool = False):
    if text.startswith("[") and not in_flow:
        if not text.endswith("]"):
            raise YAMLSubsetError(f"line {number}: unterminated flow list")
        parts = split_flow_list(text[1:-1], number)
        if parts and not parts[-1].strip():
            parts.pop()  # trailing comma
        if any(not p.strip() for p in parts):
            raise YAMLSubsetError(f"line {number}: empty flow list item")
        return [parse_yaml_scalar(p.strip(), number, in_flow=True) for p in parts]
    if text[0] in "\"'":
        if len(text) < 2 or text[-1] != text[0]:
            raise YAMLSubsetError(f"line {number}: unterminated quoted string")
        if text[0] == "'":
            return text[1:-1].replace("''", "'")
        try:
            return json.loads(text)
        except ValueError:
            raise YAMLSubsetError(f"line {number}: unsupported escape in {text}") from None
    if text[0] in "[]{}&*!|>%@`?" or ": " in text or text.endswith(":") or (in_flow and text[0] == "-" and text[1:2] == " "):
        raise YAMLSubsetError(f"line {number}: unsupported YAML syntax without PyYAML: {text}")
    if text in YAML_NULL:
        return None
    if text in YAML_BOOL:
        return YAML_BOOL[text]
    if YAML_INT.match(text):
        return int(text)
    return text


def split_flow_list(inner: str, number: int) -> list[str]:
    parts: list[str] = []
    current: list[str] = []
    quote = None
    for ch in inner:
        if quote:
            if ch == quote:
                quote = None
        elif ch in "'\"" and not "".join(current).strip():
            quote = ch
        elif ch == ",":
            parts.append("".join(current))
            current = []
            continue
        current.append(ch)
    if quote:
        raise YAMLSubsetError(f"line {number}: unterminated quoted string in flow list")
    parts.append("".join(current))
    return [] if len(parts) == 1 and not parts[0].strip() else parts


# --- Loading -----------------------------------------------------------------


def load_yaml(path: Path, report: Report, where: str) -> dict:
    try:
        data = parse_yaml(path.read_text(encoding="utf-8"))
    except (OSError, *YAML_ERRORS) as exc:
        report.error(where, f"cannot read {path.name}: {exc}")
        return {}
    if data is None:
        return {}
    if not isinstance(data, dict):
        report.error(where, f"{path.name} must be a mapping")
        return {}
    return data


def load_config(omtkc: Path, report: Report) -> dict:
    config_path = omtkc / "config.yaml"
    if not config_path.is_file():
        report.error("config.yaml", "missing")
        return {}
    config = load_yaml(config_path, report, "config.yaml")
    if config.get("schema") != SCHEMA:
        report.error("config.yaml", f"schema must be '{SCHEMA}'")
    return config


def repo_root(omtkc: Path, config: dict) -> Path:
    return (omtkc / str(config.get("repo_root", ".."))).resolve()


def snapshot_label(config: dict) -> str | None:
    """`repository@commit` for a .omtkc/ copied away from its repository, else None."""
    snapshot = config.get("snapshot")
    if not isinstance(snapshot, dict):
        return None
    return f"{snapshot.get('repository', '?')}@{snapshot.get('commit', '?')}"


def walk_elements(omtkc: Path, report: Report) -> list[Element]:
    elements: list[Element] = []

    def visit(directory: Path) -> None:
        for child in sorted(p for p in directory.iterdir() if p.is_dir()):
            if child.name.startswith((".", "_")):
                continue
            rel = child.relative_to(omtkc).as_posix()
            meta_path = child / "meta.yaml"
            meta = load_yaml(meta_path, report, rel) if meta_path.is_file() else {}
            elements.append(Element(rel, child, meta))
            visit(child)

    visit(omtkc)
    return elements


# --- TikZ scanning ------------------------------------------------------------


def strip_comments(source: str) -> str:
    return "\n".join(re.sub(r"(?<!\\)%.*", "", line) for line in source.splitlines())


def skip_balanced(text: str, start: int, opening: str, closing: str) -> int:
    """Return the index after the bracket group starting at text[start]."""
    depth = 0
    i = start
    while i < len(text):
        ch = text[i]
        if ch == "\\":
            i += 2
            continue
        if ch in "{" and opening != "{":
            i = skip_balanced(text, i, "{", "}")
            continue
        if ch == opening:
            depth += 1
        elif ch == closing:
            depth -= 1
            if depth == 0:
                return i + 1
        i += 1
    return len(text)


def split_options(options: str) -> list[str]:
    """Top-level comma-separated keys of a TikZ option list (without brackets)."""
    parts: list[str] = []
    current: list[str] = []
    depth = 0
    for ch in options:
        if ch in "{[":
            depth += 1
        elif ch in "}]":
            depth -= 1
        if ch == "," and depth == 0:
            parts.append("".join(current).strip())
            current = []
        else:
            current.append(ch)
    parts.append("".join(current).strip())
    return [p for p in parts if p]


def node_ids(source: str) -> list[str]:
    """Named \\node IDs: `\\node[opts] (id) at (x,y)`, `\\node at (x,y) (id)`, or `name=id`."""
    text = strip_comments(source)
    ids: list[str] = []
    for match in re.finditer(r"\\node\b", text):
        i = match.end()
        found = None
        after_at = False
        while i < len(text) and found is None:
            while i < len(text) and text[i].isspace():
                i += 1
            if text.startswith("[", i):
                end = skip_balanced(text, i, "[", "]")
                for option in split_options(text[i + 1 : end - 1]):
                    key, _, value = option.partition("=")
                    if key.strip() == "name" and value.strip():
                        found = value.strip().strip("{}")
                i = end
            elif text.startswith("at", i) and not text[i + 2 : i + 3].isalnum():
                after_at = True
                i += 2
            elif text.startswith("(", i):
                end = text.find(")", i)
                if end == -1:
                    break
                if not after_at:
                    found = text[i + 1 : end].strip()
                after_at = False
                i = end + 1
            else:
                break
        if found:
            ids.append(found)
    return ids


ARROW_TIP = r"(?:[<>|]+|[A-Za-z]+(?:\[[^\]]*\])?|\{[^}]*\})"
ARROW_KEY = re.compile(rf"^(?:{ARROW_TIP})?-(?:{ARROW_TIP})?$")
LABEL_NODE = re.compile(r"\bnode\b(?:\s*\[[^\]]*\]|\s*\([^)]*\))*\s*\{\s*[^}\s]")


def has_arrow(options: str) -> bool:
    return any(
        ARROW_KEY.match(key) and key != "-" and "=" not in key for key in split_options(options)
    )


def unlabeled_edges(source: str) -> list[str]:
    """Arrowed \\draw / \\path statements (or edge operations) without a text label."""
    text = strip_comments(source)
    found = []
    for match in re.finditer(r"\\(draw|path)\b(.*?);", text, re.S):
        body = match.group(2)
        options = ""
        if body.lstrip().startswith("["):
            start = body.index("[")
            options = body[start + 1 : skip_balanced(body, start, "[", "]") - 1]
        edge_options = re.findall(r"\bedge\s*\[([^\]]*)\]", body)
        arrowed = has_arrow(options) or any(has_arrow(o) for o in edge_options)
        if arrowed and not LABEL_NODE.search(body):
            found.append(" ".join(("\\" + match.group(1) + body + ";").split()))
    return found


# --- Markdown links -----------------------------------------------------------


def local_links(markdown: str) -> list[str]:
    targets = []
    for target in LINK_PATTERN.findall(markdown):
        if re.match(r"^[a-z][a-z0-9+.-]*:", target, re.I) or target.startswith("#"):
            continue
        targets.append(target.split("#", 1)[0])
    return targets


def resolved_links(md_path: Path) -> set[Path]:
    text = md_path.read_text(encoding="utf-8")
    return {(md_path.parent / target).resolve() for target in local_links(text)}


# --- Commands -----------------------------------------------------------------


def check(omtkc: Path) -> Report:
    report = Report()
    if not omtkc.is_dir():
        report.error(str(omtkc), "directory not found (run from the analyzed repository root)")
        return report
    config = load_config(omtkc, report)
    # A snapshot has no local repository, so source paths cannot be checked.
    root = None if snapshot_label(config) else repo_root(omtkc, config)
    elements = walk_elements(omtkc, report)
    by_path = {e.path: e for e in elements}

    index = omtkc / "index.md"
    if not index.is_file():
        report.error("index.md", "missing")
        index_links: set[Path] = set()
    else:
        index_links = resolved_links(index)

    for e in elements:
        check_element(e, omtkc, root, by_path, index_links, report)

    for md in sorted(omtkc.rglob("*.md")):
        rel = md.relative_to(omtkc).as_posix()
        for target in local_links(md.read_text(encoding="utf-8")):
            if not (md.parent / target).exists():
                report.error(rel, f"broken link '{target}'")
    return report


def check_element(
    e: Element,
    omtkc: Path,
    root: Path | None,
    by_path: dict[str, Element],
    index_links: set[Path],
    report: Report,
) -> None:
    where = e.path
    name = e.directory.name
    if not ID_PATTERN.match(name):
        report.error(where, "directory name must be kebab-case")
    description = e.directory / "description.md"
    if not description.is_file():
        report.error(where, "missing description.md")
    if not (e.directory / "meta.yaml").is_file():
        report.error(where, "missing meta.yaml")
        return
    if e.kind not in KINDS:
        report.error(where, f"kind must be one of {sorted(KINDS)}")
    if e.status not in STATUSES:
        report.error(where, f"status must be one of {sorted(STATUSES)}")

    child_dirs = sorted(
        p.name for p in e.directory.iterdir() if p.is_dir() and not p.name.startswith((".", "_"))
    )
    active_children = sorted(
        c for c in child_dirs if by_path.get(f"{e.path}/{c}", e).status == "active"
    )
    declared = e.meta.get("children") or []
    if sorted(declared) != child_dirs:
        report.error(where, f"meta children {sorted(declared)} != child directories {child_dirs}")

    sources = e.meta.get("sources") or []
    if not sources and e.status == "active":
        report.warn(where, "no sources recorded")
    if root is not None:
        for source in sources:
            if not (root / str(source).split("#", 1)[0]).exists():
                report.error(where, f"source not found: {source}")

    ancestors = {"/".join(e.path.split("/")[:i]) for i in range(1, e.path.count("/") + 1)}
    for ref in e.meta.get("refs") or []:
        if ref not in by_path:
            report.error(where, f"ref target not found: {ref}")
        elif ref in ancestors:
            report.warn(where, f"ref points to its own ancestor: {ref}")
        elif e.path not in (by_path[ref].meta.get("refs") or []):
            report.warn(where, f"ref to {ref} is not reciprocated")

    links = resolved_links(description) if description.is_file() else set()
    parent_doc = omtkc / "index.md" if "/" not in e.path else e.directory.parent / "description.md"
    if description.is_file() and parent_doc.resolve() not in links:
        report.error(where, f"description.md does not link to its parent ({parent_doc.name})")
    if "/" not in e.path and e.status == "active" and description.resolve() not in index_links:
        report.error("index.md", f"does not link to perspective {e.path}/description.md")

    tikz = e.directory / "diagram.tikz"
    if e.kind == "leaf":
        if tikz.exists():
            report.error(where, "leaf has diagram.tikz; use kind: group")
        if child_dirs:
            report.error(where, "leaf has child directories; use kind: group")
        return
    if e.kind != "group":
        return
    if not tikz.is_file():
        report.error(where, "group is missing diagram.tikz")
        return

    source_text = tikz.read_text(encoding="utf-8")
    ids = node_ids(source_text)
    duplicates = sorted({i for i in ids if ids.count(i) > 1})
    if duplicates:
        report.error(where, f"duplicate node IDs: {duplicates}")
    semantic = sorted({i for i in ids if not i.startswith("_")})
    for node in semantic:
        if not ID_PATTERN.match(node):
            report.error(where, f"node ID '{node}' is not kebab-case (prefix decorative IDs with '_')")
    missing_dirs = sorted(set(semantic) - set(child_dirs))
    if missing_dirs:
        report.error(where, f"semantic nodes without child directories: {missing_dirs}")
    missing_nodes = sorted(set(active_children) - set(semantic))
    if missing_nodes:
        report.error(where, f"active children not drawn in diagram.tikz: {missing_nodes}")
    retired_drawn = sorted(set(semantic) & (set(child_dirs) - set(active_children)))
    if retired_drawn:
        report.error(where, f"retired children still drawn: {retired_drawn}")
    for edge in unlabeled_edges(source_text):
        report.warn(where, f"edge without label: {edge}")

    for child in active_children:
        if (e.directory / child / "description.md").resolve() not in links:
            report.error(where, f"description.md does not link to child {child}")
    if (e.directory / "diagram.svg").resolve() not in links:
        report.error(where, "description.md does not embed diagram.svg")

    render = e.meta.get("render") or {}
    for image in ("diagram.svg", "diagram.png"):
        if not (e.directory / image).is_file():
            report.error(where, f"missing {image}")
    if render.get("check") not in CHECK_STATES:
        report.error(where, "render.check must be pass or fail")
    elif render["check"] == "fail":
        report.error(where, "render.check is fail; existing images are stale")
    if render.get("tikz_sha256") != sha256(tikz):
        report.error(where, "diagram.tikz changed after the recorded render (stale SVG/PNG)")
    if render.get("visual") not in VISUAL_STATES:
        report.error(where, "render.visual must be inspected or pending")
    elif render["visual"] == "pending":
        report.warn(where, "visual inspection pending")
    if not render.get("tikzc_version"):
        report.warn(where, "render.tikzc_version not recorded")


def tree(omtkc: Path) -> int:
    report = Report()
    if not omtkc.is_dir():
        print(f"ERROR {omtkc}: directory not found (run from the analyzed repository root)", file=sys.stderr)
        return 1
    config = load_config(omtkc, report)
    elements = walk_elements(omtkc, report)
    print(f"{omtkc}  (language: {config.get('language', '?')})")
    for e in elements:
        depth = e.path.count("/")
        render = e.meta.get("render") or {}
        state = ""
        if e.kind == "group":
            state = f"  check={render.get('check', '?')} visual={render.get('visual', '?')}"
        retired = "  [retired]" if e.status == "retired" else ""
        commit = f"  @{e.meta['analyzed_commit']}" if e.meta.get("analyzed_commit") else ""
        print(f"{'  ' * depth}- {e.directory.name} ({e.kind or '?'}){commit}{state}{retired}")
    for line in report.errors:
        print(line, file=sys.stderr)
    return 1 if report.errors else 0


def stale(omtkc: Path) -> int:
    report = Report()
    if not omtkc.is_dir():
        print(f"ERROR {omtkc}: directory not found (run from the analyzed repository root)", file=sys.stderr)
        return 1
    config = load_config(omtkc, report)
    if label := snapshot_label(config):
        print(f"Snapshot of {label}; stale needs the repository itself.")
        return 0
    root = repo_root(omtkc, config)
    elements = walk_elements(omtkc, report)
    changed_any = False
    covered: set[str] = set()
    commits: set[str] = set()
    for e in elements:
        if e.status != "active":
            continue
        sources = [str(s).split("#", 1)[0] for s in e.meta.get("sources") or []]
        if e.kind == "leaf":
            covered.update(sources)  # group sources are wiring; leaves define coverage
        commit = e.meta.get("analyzed_commit")
        if not commit:
            print(f"UNKNOWN {e.path}: no analyzed_commit")
            changed_any = True
            continue
        commits.add(str(commit))
        if not sources:
            continue
        changed = git_changed_files(root, str(commit), sources)
        if changed is None:
            print(f"UNKNOWN {e.path}: cannot diff against {commit}")
            changed_any = True
        elif changed:
            print(f"STALE   {e.path}: {', '.join(changed)}")
            changed_any = True
    try:
        omtkc_prefix = omtkc.resolve().relative_to(root).as_posix() + "/"
    except ValueError:
        omtkc_prefix = None
    scope = [str(s) for s in config.get("scope") or []]
    untracked = git_untracked_files(root)
    for commit in sorted(commits):
        changed = (git_changed_files(root, commit, ["."]) or []) + untracked
        uncovered = sorted(
            f for f in set(changed)
            if not any(f == s or f.startswith(s.rstrip("/") + "/") for s in covered)
            and not (omtkc_prefix and f.startswith(omtkc_prefix))
            and (not scope or any(f == s or f.startswith(s.rstrip("/") + "/") for s in scope))
        )
        for f in uncovered:
            print(f"NEW     {f}: changed since {commit} and not covered by any leaf")
            changed_any = True
    if not changed_any:
        print("No changes detected in recorded sources.")
    for line in report.errors:
        print(line, file=sys.stderr)
    return 1 if report.errors else 0


def stamp(group: Path, check_state: str, visual: str) -> int:
    meta_path = group / "meta.yaml"
    tikz = group / "diagram.tikz"
    if not meta_path.is_file() or not tikz.is_file():
        print(f"ERROR {group}: needs meta.yaml and diagram.tikz", file=sys.stderr)
        return 1
    result = subprocess.run(["tikzc", "--version"], capture_output=True, text=True)
    version = result.stdout.split()[-1] if result.returncode == 0 and result.stdout.split() else None
    # Replace only the top-level render block so the rest of meta.yaml keeps its layout.
    lines = meta_path.read_text(encoding="utf-8").splitlines()
    kept: list[str] = []
    in_render = False
    for line in lines:
        if re.match(r"^render\s*:", line):
            in_render = True
            continue
        if in_render and (line.startswith((" ", "\t")) or not line.strip()):
            continue
        in_render = False
        kept.append(line)
    while kept and not kept[-1].strip():
        kept.pop()
    block = [
        "render:",
        f"  tikz_sha256: {sha256(tikz)}",
        f"  tikzc_version: {version or 'null'}",
        f"  check: {check_state}",
        f"  visual: {visual}",
    ]
    meta_path.write_text("\n".join(kept + block) + "\n", encoding="utf-8")
    parse_yaml(meta_path.read_text(encoding="utf-8"))
    print(f"{meta_path}: render updated ({check_state}, {visual}, tikzc {version})")
    return 0


def git_changed_files(root: Path, commit: str, paths: list[str]) -> list[str] | None:
    result = subprocess.run(
        ["git", "-C", str(root), "diff", "--name-only", commit, "--", *paths],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        return None
    return [line for line in result.stdout.splitlines() if line]


def git_untracked_files(root: Path) -> list[str]:
    result = subprocess.run(
        ["git", "-C", str(root), "ls-files", "--others", "--exclude-standard"],
        capture_output=True,
        text=True,
    )
    return [line for line in result.stdout.splitlines() if line] if result.returncode == 0 else []


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="command", required=True)
    for name in ("check", "tree", "stale"):
        p = sub.add_parser(name)
        p.add_argument("omtkc_dir", nargs="?", default=".omtkc", type=Path)
    p = sub.add_parser("stamp")
    p.add_argument("group_dir", type=Path)
    p.add_argument("--check", required=True, choices=sorted(CHECK_STATES))
    p.add_argument("--visual", required=True, choices=sorted(VISUAL_STATES))
    p = sub.add_parser("hash")
    p.add_argument("files", nargs="+", type=Path)
    args = parser.parse_args(argv)

    if args.command == "hash":
        for f in args.files:
            print(f"{sha256(f)}  {f}")
        return 0
    if args.command == "stamp":
        return stamp(args.group_dir, args.check, args.visual)
    if args.command == "tree":
        return tree(args.omtkc_dir)
    if args.command == "stale":
        return stale(args.omtkc_dir)
    report = check(args.omtkc_dir)
    for line in report.errors + report.warnings:
        print(line)
    print(f"{len(report.errors)} error(s), {len(report.warnings)} warning(s)")
    return 1 if report.errors else 0


if __name__ == "__main__":
    sys.exit(main())
