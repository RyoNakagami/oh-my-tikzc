# `.omtkc/` format (schema `omtkc/1`)

`.omtkc/` (short for oh-my-tikzc) is this package's documentation tree, analogous to oh-my-mermaid's `.omm/`. It is meant to be committed with the analyzed repository and reviewed with ordinary `git diff`. `scripts/omtkc.py check` validates everything marked **checked** below.

## Layout

```text
.omtkc/
  config.yaml                    # required
  index.md                       # required: entry point
  <perspective>/                 # top-level element
    description.md               # required for every element
    meta.yaml                    # required for every element
    diagram.tikz                 # groups only
    diagram.svg                  # groups only, rendered by tikzc
    diagram.png                  # groups only, rendered by tikzc
    context.md constraint.md concern.md todo.md note.md   # optional
    <child>/                     # one per semantic node in diagram.tikz
      description.md
      meta.yaml
```

Directory names are English kebab-case (`^[a-z0-9]+(-[a-z0-9]+)*$`, **checked**). Directories starting with `.` or `_` are ignored by the checker and may hold scratch material. They are unrelated to `_`-prefixed node IDs: decorative and context nodes never get directories.

## `config.yaml`

```yaml
schema: omtkc/1        # checked
language: ja         # prose and label language; reuse it on refresh
repo_root: ..        # optional; analyzed repository root relative to .omtkc/ (default ..)
scope:               # optional; repository paths the documentation is meant to cover
  - src/
  - vscode-extension/src/
```

A `.omtkc/` copied out of its repository, for example as a published sample, declares where it came from instead of `repo_root`. Its source links must then be absolute permalinks at that commit:

```yaml
snapshot:
  repository: https://github.com/RyoNakagami/tikzc
  commit: ef3a589541731a9c7098921c25f4770d86ac5d37
```

With `snapshot`, `check` skips the source-existence check and `stale` does nothing; everything else is checked as usual.

`scope` limits `omtkc.py stale`'s `NEW` lines to files inside these paths, so changelogs, lock files, tests, and docs do not appear as uncovered. Without it, every changed file is considered.

## `meta.yaml`

```yaml
kind: group                      # group | leaf (checked)
status: active                   # active | retired (default active, checked)
sources:                         # repository-root-relative paths that justify this element (checked to exist)
  - src/cli.rs
  - src/render/                  # a directory covers everything below it
children: [parser, renderer]     # must equal the child directories, including retired ones (checked)
refs: [data-flow/renderer]       # the same component elsewhere, as a path below .omtkc/ (checked, must be mutual)
analyzed_commit: 38ccdb6         # HEAD when this element was last analyzed
working_tree_dirty: false        # true if uncommitted changes were part of the analysis
render:                          # groups only (checked)
  tikz_sha256: 3f5c…             # written by `omtkc.py stamp`; do not edit by hand
  tikzc_version: 1.2.0
  check: pass                    # pass | fail
  visual: inspected              # inspected | pending
```

Write the `render` block with `uv run scripts/omtkc.py stamp <group-dir> --check pass --visual inspected` after the final render and inspection. It records the hash of `diagram.tikz` and the installed tikzc version.

- `sources` may carry a symbol suffix such as `src/cli.rs#dispatch` to name the relevant part of a shared file; only the path is checked, and `stale` works per file.
- A **leaf** lists the files that implement it. A **group** lists only the files that implement the relationships drawn in its diagram (dispatch, wiring, shared types), not the union of its children; broad directories make `stale` flag the group on every change.
- An **external system** lists the code that contacts it (client, configuration). A user-supplied input (for example a `.tikz` file) lists the code that reads it and, optionally, an example file. A file a command writes to a user-chosen path is a `store` leaf whose sources are the writing code. Never invent local paths.
- `children`: a leaf has none; a group lists all child directories, retired ones included.
- `refs` connect appearances of the same component in different places, including a leaf that is detailed by a whole perspective (`refs: [data-flow]`). Refs are mutual: add the reverse entry to the target (a one-way ref is a warning). Appearances that show different aspects of one component may have different `sources`.
- `analyzed_commit` is `git rev-parse --short HEAD` at the start of the analysis, and `working_tree_dirty` reflects `git status --porcelain` at that time, before `.omtkc/` was written. `omtkc.py stale` runs `git diff <commit> -- <sources>`. Update both only for elements that were actually re-read.
- `render.tikz_sha256` makes stale images detectable: if `diagram.tikz` changes without a new render, `check` reports an error. Modification times are not used because checkouts reset them.
- If `tikzc check` or rendering fails, or tikzc is unavailable, set `check: fail` and say so in the description; existing images are stale. The checker then reports an error by design: unrendered documentation is not complete.
- If no image-reading tool was available, set `visual: pending` (a warning, not an error).

## YAML subset

Write `config.yaml` and `meta.yaml` in this subset so the checker reads them the same way with or without PyYAML:

- mappings with plain keys (`kind:`, `tikz_sha256:`), nested by space indentation
- lists of scalars, either in block form (`- src/`) or flow form (`[a, b]`)
- plain scalars, `'single'` or `"double"` quoted strings, `null`/`~`, `true`/`false`, and `#` comments

Without PyYAML, anything else (anchors, tags, multi-line `|`/`>` strings, `{...}` mappings, lists of mappings, `---` markers, tabs) is reported as an error instead of being guessed.

## Diagram ↔ directory contract (checked)

In a group's `diagram.tikz`:

- Every **semantic node** has a kebab-case ID equal to a child directory name: `\node[block] (command-router) …`.
- **Decorative nodes** (legends, frames, notes, layout helpers) have no ID or an ID starting with `_`: `\node (_legend) …`. `\coordinate` names are never semantic.
- **Context nodes** show something outside this element that it talks to, typically a sibling or parent-level component. Use the `context` style and an ID `_ctx-<name>`, and link the real element from the description (for example `[Element store](../element-store/description.md)`). Do not create child directories or refs for them.
- IDs are recognised in `\node[opts] (id)`, `\node (id) at (x,y)`, `\node at (x,y) (id)`, and `name=id`.
- Every active child is drawn; a retired child is not drawn.
- Node IDs are unique.
- Arrowed edges (`->`, `<-`, `<->`, `-latex`, `edge[->]`, …) carry a `node` with non-empty text stating the relationship (unlabeled edges are warnings). An arrow style defined with `.style` is not detected.
- If an existing relationship is left out to keep the diagram readable, list it under "Omitted edges" in the description.

## Navigation contract (checked)

- `index.md` links every active perspective's `description.md`.
- Every `description.md` links its parent: `../index.md` for a perspective, `../description.md` below it.
- A group's `description.md` embeds `diagram.svg` and links each active child's `description.md`.
- Every relative Markdown link in `.omtkc/` resolves.

Source links point back into the repository. With `.omtkc/` at the repository root, an element at depth *d* (a perspective is depth 1) prefixes repository paths with *d* + 1 copies of `../`: `../../src/cli.rs` from a perspective, `../../../src/cli.rs` from its child. Write a symbol as code text after the link:

```markdown
- [`src/cli.rs`](../../src/cli.rs) — `dispatch`, `run`
```

`index.md` states scope, analyzed commit, working-tree state, language, perspectives with links and questions, and render status (tikzc version, any `visual: pending`). The checker result is reported to the user rather than stored, because it can only be known after `index.md` is written.

## Field vocabulary

The seven fields of oh-my-mermaid are kept. Write only those with evidence; omit empty files.

| File | Content |
| --- | --- |
| `description.md` | Role, boundary, source paths with symbols, and evidence for each relationship |
| `diagram.tikz` | The element's internal structure (groups only) |
| `context.md` | Why it is designed this way, when documented or evident |
| `constraint.md` | Requirements or invariants the code enforces |
| `concern.md` | Evidenced risks; mark the node with the `concern` style |
| `todo.md` | Work recorded in the code or docs (TODO comments, issues) |
| `note.md` | Other useful facts, including human notes; never overwrite these |

## Visual vocabulary

Styles are defined in `assets/architecture.tikz`. Each is distinguishable without color.

| Style | Shape | Use for |
| --- | --- | --- |
| `block` | rounded rectangle | ordinary internal component |
| `entry` | thick border | entry points: CLI, HTTP handler, extension activation |
| `store` | cylinder | persistent storage: files, database, cache |
| `external` | dashed border | systems outside the repository |
| `concern` | dash-dot border with `!` | component with a documented concern |
| `context` | dotted gray border | a component outside this element (ID `_ctx-…`, not semantic) |

Roles combine: write `\node[entry,concern]` or `\node[store,concern]`; the later style keeps the earlier one's border width or shape and adds the concern color, dash pattern, and mark. Copy the template's whole option block, through the closing `]`, into every diagram so styles stay consistent.

## Retirement

When a component disappears, set `status: retired` in its `meta.yaml`, remove its node from the parent diagram, add a line explaining the retirement to its description, and keep the directory if it holds human-authored material. Otherwise it may be deleted together with its `children` entry.
