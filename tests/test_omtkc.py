"""Tests for skills/tikzc-architecture/scripts/omtkc.py.

Run from the repository root:
    uv run --with pyyaml python -m unittest discover -s tests

Without PyYAML, the comparisons against it are skipped.
"""

from __future__ import annotations

import contextlib
import hashlib
import importlib.util
import io
import subprocess
import sys
import tempfile
import textwrap
import unittest
from pathlib import Path
from unittest import mock

SCRIPT = Path(__file__).resolve().parents[1] / "skills" / "tikzc-architecture" / "scripts" / "omtkc.py"
spec = importlib.util.spec_from_file_location("omtkc", SCRIPT)
omtkc = importlib.util.module_from_spec(spec)
sys.modules["omtkc"] = omtkc
spec.loader.exec_module(omtkc)

DIAGRAM = textwrap.dedent(
    r"""
    \begin{tikzpicture}[block/.style={draw,label={[font=\tiny]30:!}}]
      \node[block] (cli) at (0,0) {CLI\\src/cli.rs};
      \node[block, fill=blue!5] (renderer) at (4,0) {Renderer};
      \node (_legend) at (2,-2) {legend};
      \node at (2,-3) {note};
      % \node (commented-out) {x};
      \draw[->] (cli) -- node[above] {source} (renderer);
    \end{tikzpicture}
    """
)


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(textwrap.dedent(text).lstrip(), encoding="utf-8")


def git(root: Path, *args: str) -> str:
    return subprocess.run(
        ["git", "-C", str(root), *args], check=True, capture_output=True, text=True
    ).stdout.strip()


class Fixture:
    """A small analyzed repository with a valid .omtkc/ tree."""

    def __init__(self, root: Path) -> None:
        self.root = root
        self.omtkc = root / ".omtkc"
        write(root / "src" / "cli.rs", "fn main() {}\n")
        write(root / "src" / "render.rs", "pub fn render() {}\n")
        git(root, "init", "-q")
        git(root, "-c", "user.name=t", "-c", "user.email=t@example.com", "add", ".")
        git(root, "-c", "user.name=t", "-c", "user.email=t@example.com", "commit", "-qm", "init")
        self.commit = git(root, "rev-parse", "--short", "HEAD")

        write(self.omtkc / "config.yaml", "schema: omtkc/1\nlanguage: en\n")
        write(self.omtkc / "index.md", "# Index\n\n- [Overall](overall-architecture/description.md)\n")
        group = self.omtkc / "overall-architecture"
        write(group / "diagram.tikz", DIAGRAM)
        (group / "diagram.svg").write_text("<svg/>", encoding="utf-8")
        (group / "diagram.png").write_bytes(b"png")
        digest = hashlib.sha256((group / "diagram.tikz").read_bytes()).hexdigest()
        write(
            group / "meta.yaml",
            f"""
            kind: group
            status: active
            sources: [src/cli.rs, src/render.rs]
            children: [cli, renderer]
            analyzed_commit: {self.commit}
            render:
              tikz_sha256: {digest}
              tikzc_version: 1.2.0
              check: pass
              visual: inspected
            """,
        )
        write(
            group / "description.md",
            """
            [Index](../index.md)

            ![diagram](diagram.svg)

            - [CLI](cli/description.md)
            - [Renderer](renderer/description.md)
            """,
        )
        for name, source in (("cli", "src/cli.rs"), ("renderer", "src/render.rs")):
            write(group / name / "meta.yaml", f"kind: leaf\nsources: [{source}]\nanalyzed_commit: {self.commit}\n")
            write(group / name / "description.md", f"[Up](../description.md) — see [{source}](../../../{source})\n")

    @property
    def group(self) -> Path:
        return self.omtkc / "overall-architecture"


class OmtkcTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.fx = Fixture(Path(self._tmp.name))

    def tearDown(self) -> None:
        self._tmp.cleanup()

    def errors(self) -> list[str]:
        return omtkc.check(self.fx.omtkc).errors


class NodeIdTests(unittest.TestCase):
    def test_extracts_named_nodes_with_nested_options(self) -> None:
        self.assertEqual(omtkc.node_ids(DIAGRAM), ["cli", "renderer", "_legend"])

    def test_other_node_forms(self) -> None:
        source = r"\node at (0,0) (late-id) {A}; \node[draw,name=named] {B}; \coordinate (c) at (1,1);"
        self.assertEqual(omtkc.node_ids(source), ["late-id", "named"])

    def test_detects_unlabeled_edges(self) -> None:
        source = r"\draw[->] (a) -- (b); \draw[->] (a) -- node {x} (b); \draw (a) -- (b);"
        self.assertEqual(omtkc.unlabeled_edges(source), [r"\draw[->] (a) -- (b);"])

    def test_arrow_variants_and_empty_labels(self) -> None:
        source = "\n".join(
            [
                r"\draw[thick,-latex] (a) -- (b);",
                r"\path[<->] (a) -- (b);",
                r"\path (a) edge[->] (b);",
                r"\draw[->] (a) -- node[coordinate] {} (b);",
                r"\draw[line width=1pt, dashed] (a) -- (b);",
                r"\draw[{Stealth[length=2mm]}-] (a) -- node[above] {ok} (b);",
            ]
        )
        self.assertEqual(len(omtkc.unlabeled_edges(source)), 4)


class CheckTests(OmtkcTestCase):
    def test_valid_fixture_passes(self) -> None:
        report = omtkc.check(self.fx.omtkc)
        self.assertEqual(report.errors, [])
        self.assertEqual(report.warnings, [])

    def test_node_without_child_directory(self) -> None:
        tikz = self.fx.group / "diagram.tikz"
        tikz.write_text(DIAGRAM.replace("(_legend)", "(legend)"), encoding="utf-8")
        self.assertTrue(any("semantic nodes without child directories: ['legend']" in e for e in self.errors()))
        self.assertTrue(any("stale SVG/PNG" in e for e in self.errors()))

    def test_child_directory_not_in_meta_or_diagram(self) -> None:
        write(self.fx.group / "extra" / "meta.yaml", "kind: leaf\nsources: [src/cli.rs]\n")
        write(self.fx.group / "extra" / "description.md", "[Up](../description.md)\n")
        errors = self.errors()
        self.assertTrue(any("meta children" in e for e in errors))
        self.assertTrue(any("active children not drawn" in e for e in errors))

    def test_retired_child_may_be_absent_from_diagram(self) -> None:
        write(self.fx.group / "old" / "meta.yaml", "kind: leaf\nstatus: retired\n")
        write(self.fx.group / "old" / "description.md", "[Up](../description.md) Retired.\n")
        meta = self.fx.group / "meta.yaml"
        meta.write_text(meta.read_text().replace("[cli, renderer]", "[cli, old, renderer]"))
        self.assertEqual(self.errors(), [])

    def test_broken_link_and_missing_source(self) -> None:
        cli = self.fx.group / "cli"
        write(cli / "description.md", "[Up](../description.md) [gone](../../../src/gone.rs)\n")
        write(cli / "meta.yaml", "kind: leaf\nsources: [src/gone.rs]\n")
        errors = self.errors()
        self.assertTrue(any("broken link" in e for e in errors))
        self.assertTrue(any("source not found: src/gone.rs" in e for e in errors))

    def test_navigation_links_required(self) -> None:
        write(self.fx.group / "renderer" / "description.md", "No parent link.\n")
        write(self.fx.omtkc / "index.md", "# Index\n")
        errors = self.errors()
        self.assertTrue(any("renderer: description.md does not link to its parent" in e for e in errors))
        self.assertTrue(any("index.md: does not link to perspective" in e for e in errors))

    def test_failed_render_and_pending_visual(self) -> None:
        meta = self.fx.group / "meta.yaml"
        meta.write_text(meta.read_text().replace("visual: inspected", "visual: pending"))
        report = omtkc.check(self.fx.omtkc)
        self.assertEqual(report.errors, [])
        self.assertTrue(any("visual inspection pending" in w for w in report.warnings))
        meta.write_text(meta.read_text().replace("check: pass", "check: fail"))
        self.assertTrue(any("render.check is fail" in e for e in self.errors()))

    def test_one_way_ref_warns(self) -> None:
        meta = self.fx.group / "cli" / "meta.yaml"
        meta.write_text(meta.read_text() + "refs: [overall-architecture/renderer]\n")
        report = omtkc.check(self.fx.omtkc)
        self.assertEqual(report.errors, [])
        self.assertTrue(any("not reciprocated" in w for w in report.warnings))

    def test_stamp_records_render(self) -> None:
        (self.fx.group / "diagram.tikz").write_text(DIAGRAM + "% edited\n", encoding="utf-8")
        self.assertTrue(any("stale SVG/PNG" in e for e in self.errors()))
        meta = self.fx.group / "meta.yaml"
        before = meta.read_text().split("render:")[0]
        with contextlib.redirect_stdout(io.StringIO()):
            omtkc.stamp(self.fx.group, "pass", "inspected")
        self.assertEqual(self.errors(), [])
        self.assertTrue(meta.read_text().startswith(before), "lines outside render must not change")

    def test_missing_directory_does_not_crash(self) -> None:
        missing = self.fx.root / "nope"
        with contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(omtkc.tree(missing), 1)
            self.assertEqual(omtkc.stale(missing), 1)

    def test_snapshot_skips_source_checks(self) -> None:
        moved = self.fx.root / "examples" / ".omtkc"
        moved.parent.mkdir()
        self.fx.omtkc.rename(moved)
        config = moved / "config.yaml"
        self.assertTrue(any("source not found" in e for e in omtkc.check(moved).errors))
        config.write_text(config.read_text() + "snapshot:\n  repository: https://example.com/r\n  commit: abc\n")
        self.assertFalse(any("source not found" in e for e in omtkc.check(moved).errors))
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            self.assertEqual(omtkc.stale(moved), 0)
        self.assertIn("Snapshot of https://example.com/r@abc", out.getvalue())

    def test_leaf_with_diagram_is_error(self) -> None:
        write(self.fx.group / "cli" / "diagram.tikz", DIAGRAM)
        self.assertTrue(any("leaf has diagram.tikz" in e for e in self.errors()))


class YamlSubsetTests(unittest.TestCase):
    SUPPORTED = textwrap.dedent(
        """
        # comment
        kind: group
        sources: [src/cli.rs#dispatch, 'src/a b.rs', "src/c.rs",]
        children: []
        scope:
        - src/   # trailing comment
        refs:
          - data-flow/renderer
        analyzed_commit: 38ccdb6
        working_tree_dirty: false
        note: it's fine
        render:
          tikz_sha256: '#3f5c'
          tikzc_version: 1.2.0
          check: ~
        """
    )

    def test_reads_supported_subset(self) -> None:
        data = omtkc.parse_yaml_subset(self.SUPPORTED)
        self.assertEqual(data["sources"], ["src/cli.rs#dispatch", "src/a b.rs", "src/c.rs"])
        self.assertEqual(data["scope"], ["src/"])
        self.assertIs(data["working_tree_dirty"], False)
        self.assertEqual(data["render"], {"tikz_sha256": "#3f5c", "tikzc_version": "1.2.0", "check": None})

    @unittest.skipIf(omtkc.yaml is None, "PyYAML not installed")
    def test_matches_pyyaml(self) -> None:
        self.assertEqual(omtkc.parse_yaml_subset(self.SUPPORTED), omtkc.yaml.safe_load(self.SUPPORTED))
        examples = Path(__file__).resolve().parents[1] / "examples"
        for path in examples.rglob("*.yaml"):
            text = path.read_text(encoding="utf-8")
            self.assertEqual(omtkc.parse_yaml_subset(text), omtkc.yaml.safe_load(text), path)

    def test_rejects_unsupported_syntax(self) -> None:
        for text in ("a: &x 1", "a: |\n  t", "a: {b: 1}", "a:\n  - b: 1", "a: b: c", "---\na: 1", "a: [b"):
            with self.subTest(text=text), self.assertRaises(omtkc.YAMLSubsetError):
                omtkc.parse_yaml_subset(text)


class WithoutPyyamlTests(OmtkcTestCase):
    def setUp(self) -> None:
        super().setUp()
        patcher = mock.patch.multiple(omtkc, yaml=None, YAML_ERRORS=(omtkc.YAMLSubsetError,))
        patcher.start()
        self.addCleanup(patcher.stop)

    def test_check_and_stamp(self) -> None:
        self.assertEqual(self.errors(), [])
        (self.fx.group / "diagram.tikz").write_text(DIAGRAM + "% edited\n", encoding="utf-8")
        with contextlib.redirect_stdout(io.StringIO()):
            omtkc.stamp(self.fx.group, "pass", "inspected")
        self.assertEqual(self.errors(), [])

    def test_unsupported_yaml_is_reported(self) -> None:
        meta = self.fx.group / "cli" / "meta.yaml"
        meta.write_text(meta.read_text() + "anchor: &a 1\n")
        self.assertTrue(any("unsupported YAML syntax" in e for e in self.errors()))


class StaleTests(OmtkcTestCase):
    def run_stale(self) -> str:
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            omtkc.stale(self.fx.omtkc)
        return out.getvalue()

    def test_no_changes(self) -> None:
        self.assertIn("No changes detected", self.run_stale())

    def test_changed_source_and_new_file(self) -> None:
        (self.fx.root / "src" / "render.rs").write_text("pub fn render2() {}\n")
        write(self.fx.root / "src" / "cache.rs", "pub struct Cache;\n")
        output = self.run_stale()
        self.assertIn("STALE   overall-architecture: src/render.rs", output)
        self.assertIn("STALE   overall-architecture/renderer: src/render.rs", output)
        self.assertNotIn("overall-architecture/cli:", output)
        self.assertIn("NEW     src/cache.rs", output)

    def test_scope_limits_new_files(self) -> None:
        config = self.fx.omtkc / "config.yaml"
        config.write_text(config.read_text() + "scope: [src/]\n")
        write(self.fx.root / "src" / "cache.rs", "pub struct Cache;\n")
        write(self.fx.root / "CHANGELOG.md", "# Changes\n")
        output = self.run_stale()
        self.assertIn("NEW     src/cache.rs", output)
        self.assertNotIn("CHANGELOG.md", output)

    def test_broad_group_source_does_not_hide_new_files(self) -> None:
        meta = self.fx.group / "meta.yaml"
        meta.write_text(meta.read_text().replace("sources: [src/cli.rs, src/render.rs]", "sources: [src/]"))
        write(self.fx.root / "src" / "cache.rs", "pub struct Cache;\n")
        self.assertIn("NEW     src/cache.rs", self.run_stale())


if __name__ == "__main__":
    unittest.main()
