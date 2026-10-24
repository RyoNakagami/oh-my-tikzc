# Getting started

[日本語](JP/getting-started.md) · [How it works](how-it-works.md)

This guide takes you from a clean machine to a committed `.omtkc/` architecture tree for your own repository, and then shows how to keep it up to date.

## 1. Install the prerequisites

oh-my-tikzc is a skill package for an AI coding agent. It needs two command-line tools:

| Tool | Why | Version |
| --- | --- | --- |
| [tikzc](https://github.com/RyoNakagami/tikzc#installation) | Compiles each `diagram.tikz` into SVG and PNG | **1.2.0 or later** |
| [uv](https://docs.astral.sh/uv/getting-started/installation/) | Runs the bundled checker `omtkc.py` and fetches PyYAML | any recent release |

Confirm that both are on your PATH:

```sh
tikzc --version   # tikzc 1.2.1
uv --version
```

tikzc renders natively with embedded fonts, so no TeX installation is needed. Releases before 1.2.0, including the old TypeScript/TeX pipeline, are not supported.

uv is optional. Without it, the checker runs under `python3` (3.10 or later). It uses PyYAML when installed and falls back to a built-in parser otherwise.

You also need an agent that reads skills: [Claude Code](https://code.claude.com/docs/en/skills) or [Codex](https://learn.chatgpt.com/docs/build-skills).

## 2. Install the skill

This repository is a plugin marketplace that both tools read. Add it, then install its `oh-my-tikzc` plugin, which contains the `tikzc-architecture` skill.

**Claude Code**:

```sh
claude plugin marketplace add RyoNakagami/oh-my-tikzc
claude plugin install oh-my-tikzc@oh-my-tikzc
```

**Codex**:

```sh
codex plugin marketplace add RyoNakagami/oh-my-tikzc
codex plugin add oh-my-tikzc@oh-my-tikzc
```

After installing, **start a new agent session** in the repository you want to document. Skills are discovered when a session starts.

### Updating the skill

```sh
# Claude Code
claude plugin marketplace update oh-my-tikzc
claude plugin update oh-my-tikzc@oh-my-tikzc

# Codex
codex plugin marketplace upgrade oh-my-tikzc
```

### Manual install

Use this to install without a marketplace, or to share the skill through a project. Clone or download this repository and run the commands from its root. Copy the **whole** `skills/tikzc-architecture/` directory: `references/`, `assets/`, `scripts/`, and `agents/` are all used at run time.

**Claude Code** (personal skill):

```sh
mkdir -p "$HOME/.claude/skills"
test ! -e "$HOME/.claude/skills/tikzc-architecture" && test ! -L "$HOME/.claude/skills/tikzc-architecture" && cp -R skills/tikzc-architecture "$HOME/.claude/skills/"
```

**Codex** (personal skill):

```sh
mkdir -p "$HOME/.agents/skills"
test ! -e "$HOME/.agents/skills/tikzc-architecture" && test ! -L "$HOME/.agents/skills/tikzc-architecture" && cp -R skills/tikzc-architecture "$HOME/.agents/skills/"
```

The `test` guards stop the copy if a skill with the same name is already installed, so an existing installation is never overwritten by accident. To upgrade, move the old directory aside, copy the new one, and delete the backup once you're satisfied.

**Project-scoped install**: copy the same directory into the target project's `.claude/skills/` (Claude Code) or `.agents/skills/` (Codex) instead. Everyone who clones the project then gets the skill.

**Windows**: copy the directory with Explorer or PowerShell into the equivalent folder under your user profile or project.

A manually installed skill has no plugin prefix: invoke it as `/tikzc-architecture` or `$tikzc-architecture` instead of the `oh-my-tikzc:tikzc-architecture` forms below.

## 3. Generate your first architecture tree

From the root of the repository you want to document, invoke the skill.

Claude Code:

```text
/oh-my-tikzc:tikzc-architecture Explain this repository's architecture.
```

Codex:

```text
$oh-my-tikzc:tikzc-architecture Explain this repository's architecture.
```

A plain request like "map this codebase with tikzc" also works. The language of your request becomes the documentation language (English by default) and is saved in `config.yaml` for later refreshes. To get Japanese documentation, ask for it:

```text
/oh-my-tikzc:tikzc-architecture Explain this repository's architecture in Japanese.
```

### Narrow the scope

A repository-wide scan always starts with an `overall-architecture` perspective. For a large repository, or when you only care about one question, say so:

```text
Use tikzc-architecture to document only the request lifecycle of src/api/.
Use tikzc-architecture to show how CLI commands are dispatched, nothing else.
Write the documentation to docs/architecture/ instead of .omtkc/.
```

### What the agent does

While it works, the agent:

1. Reads manifests, entry points, and existing docs, and records the current commit.
2. Picks perspectives that answer distinct questions, such as data flow or command dispatch.
3. Writes a description, a `meta.yaml`, and, for components with internal structure, a `diagram.tikz`.
4. Runs `tikzc check`, renders SVG/PNG, and looks at each PNG.
5. Runs `omtkc.py check` and fixes every error.

At the end it reports the root index, the perspectives it created, the render and checker results, and any open questions. [How it works](how-it-works.md) covers each step in detail.

## 4. Read the result

The output goes to `.omtkc/` at the repository root:

```text
.omtkc/
  config.yaml                  # schema, language, scope
  index.md                     # start here
  overall-architecture/
    description.md             # explanation + embedded diagram.svg
    meta.yaml                  # sources, children, analyzed commit, render state
    diagram.tikz               # editable source
    diagram.svg / diagram.png  # rendered by tikzc
    compiler/                  # one directory per node in the diagram
      description.md
      meta.yaml
      ...
```

Open `.omtkc/index.md` in any Markdown preview (VS Code, GitHub, GitLab) and follow the links down. Each group's page embeds its SVG, links to the editable `.tikz` source, and links to one page per node in the diagram. Every page links back to its parent.

The SVGs are static images: clicking a node in the picture does nothing, so navigate with the links beneath it. For a real example, browse [examples/tikzc/.omtkc/index.md](../examples/tikzc/.omtkc/index.md), the output for tikzc itself.

**Review the content.** The agent traces every edge to code and labels any inference, but a diagram explains only the code that was read. It is not a verified specification. Check the arrows you care about against the source links on each page.

## 5. Commit it

```sh
git add .omtkc
git commit -m "docs: add architecture documentation"
```

Committing `.omtkc/` makes diagram history visible in plain `git diff` and gives the next refresh a baseline. Every element records the commit it was analyzed at.

## 6. Keep it up to date

After the code changes, ask for a refresh:

```text
/oh-my-tikzc:tikzc-architecture Refresh the existing .omtkc documentation.
```

The agent runs `omtkc.py stale` to find components whose source files changed since they were last analyzed, plus changed files that no component covers yet. It then rereads only those sources and updates the affected pages and diagrams. Human-written `note.md` files, stable IDs, and untouched subtrees are preserved. Commit the result again.

## Run the checker yourself

The agent runs the checker automatically, but you can also run it directly, for example in CI or after editing a `.tikz` file by hand. `<skill>` is the installed skill directory, such as `~/.claude/plugins/cache/oh-my-tikzc/oh-my-tikzc/<version>/skills/tikzc-architecture` (Codex: under `~/.codex/plugins/cache/`) or, for a manual install, `~/.claude/skills/tikzc-architecture`.

```sh
uv run <skill>/scripts/omtkc.py check .omtkc   # structure, links, sources, render freshness
uv run <skill>/scripts/omtkc.py tree  .omtkc   # hierarchy, analyzed commit, render state
uv run <skill>/scripts/omtkc.py stale .omtkc   # what changed since each element was analyzed
```

Without uv, replace `uv run` with `python3`. `check` exits non-zero if it finds any error, so it can gate a CI job.

If you edit a `diagram.tikz` by hand, re-render it and record the new render state. Otherwise `check` will report the images as stale:

```sh
tikzc check .omtkc/overall-architecture/diagram.tikz
tikzc .omtkc/overall-architecture/diagram.tikz -f both -o .omtkc/overall-architecture/
uv run <skill>/scripts/omtkc.py stamp .omtkc/overall-architecture --check pass --visual inspected
```

## Troubleshooting

| Symptom | Cause and fix |
| --- | --- |
| The skill isn't offered or `/oh-my-tikzc:tikzc-architecture` is unknown | The session started before the install. Start a new session, and check that `claude plugin list` or `codex plugin list` shows `oh-my-tikzc` as installed. For a manual install, also check that the whole directory was copied, not only `SKILL.md`. |
| The agent says tikzc is missing or too old | Install tikzc 1.2.0 or later. The agent will not install software for you. It can still analyze the code, but it records diagrams as `check: fail` until rendering works. |
| `ERROR <group>: diagram.tikz changed after the recorded render (stale SVG/PNG)` | The `.tikz` was edited without re-rendering. Render it again and run `stamp`, as shown above. |
| `visual=pending` in `tree` output, or a `visual inspection pending` warning | The agent had no image-reading tool, so nobody looked at the PNG. Open it yourself, then stamp with `--visual inspected`. |
| `NEW <file>: … not covered by any leaf` | A file changed or was added that no component lists in `sources`. Ask for a refresh, or add a `scope:` to `config.yaml` to exclude tests and docs. |
| A label renders with an en dash instead of `--flag` | tikzc follows TeX ligatures. Write `-{}-flag` in the `.tikz` source. See [rendering.md](../skills/tikzc-architecture/references/rendering.md). |
