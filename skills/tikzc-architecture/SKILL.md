---
name: tikzc-architecture
description: Analyze a codebase into perspective-based, hierarchical architecture documentation (.omtkc/) with TikZ diagrams rendered by tikzc. Use for requests to map a repository with tikzc, explain its architecture in TikZ, or refresh or check existing .omtkc documentation. For a standalone diagram from supplied text, use the user's drawing workflow instead.
---

# Architecture that people can follow

Turn source code into a navigable explanation: an overview, relevant architectural perspectives, and details where they help a reader. Keep evidence, diagrams, and design context together in `.omtkc/`, a tree meant to be committed beside the code. Use stable English kebab-case directory and semantic node IDs. In Japanese prose use `，` and `．`.

This skill uses the external `tikzc` renderer and a bundled checker run with `uv`, or with `python3` when uv is unavailable. It does not depend on `omm`, a cloud account, or another skill. Resolve bundled paths relative to this file (`<skill>` below), regardless of the working directory.

## Establish the scope

Read the repository's instructions, manifests, entry points, and existing architecture documentation. Respect an explicitly requested subsystem or output directory; otherwise analyze the current repository and write to `.omtkc/` at its root. Exclude generated output, vendored dependencies, and secrets from exploration.

Check `tikzc --version` (1.2.0 or later is required) and `uv --version`. Read [format.md](references/format.md) and [rendering.md](references/rendering.md) before writing files. If tikzc is missing or older than 1.2.0, explain the prerequisite and link to its installation instructions; do not silently install software. Source analysis can continue, but record diagrams as `check: fail` until rendering is possible. If uv is missing, or `uv run` fails (for example offline or in a sandbox), but `python3 --version` reports 3.10 or later, run every `uv run <skill>/scripts/omtkc.py` command below as `python3 <skill>/scripts/omtkc.py` instead. In a sandbox, if `python3 -c 'import yaml'` fails, run `python3 -m pip install pyyaml` and report that you did; if the install also fails, continue without it, because PyYAML is optional. If neither is available, apply the checklist in format.md by hand and say the checker was not run.

If `.omtkc/config.yaml` exists, this is a refresh: follow [Refresh existing documentation](#refresh-existing-documentation). Otherwise create `config.yaml` with `schema: omtkc/1`, the language of the user's request (default English), and a `scope` listing the source directories you analyze, and record `git rev-parse --short HEAD` and whether `git status --porcelain` is empty.

## Choose questions before diagrams

For a repository-wide scan, begin with `overall-architecture`. Add a perspective only if it answers a different useful question supported by the code:

| Perspective | Question and evidence |
| --- | --- |
| `request-lifecycle` | How is a request handled? Follow routes, middleware, handlers, and responses. |
| `data-flow` | Where does data originate, change, and persist? Follow reads, transformations, and writes. |
| `command-surface` | How do commands dispatch? Follow the CLI parser and command handlers. |
| `dependency-map` | Which modules depend on others? Distinguish static imports from runtime calls. |
| `external-integrations` | Which external systems are contacted, and through which boundary? |
| `state-transitions` | Which events move a feature between states? Follow transition logic. |
| `pipeline` | Which stages run, in what order, and what passes between them? |
| `extension-points` | How are implementations registered, selected, and invoked? |
| `route-page-map` | How are a frontend's pages and navigation organized? |
| `storage` | With two or more stores: which data lives where? |

Catalog names are suggestions. When a perspective answers a narrower question, give it a precise kebab-case name instead (for example `preview-edit-flow` rather than a `data-flow` limited to one subsystem). Do not create a catalog of empty views. For a scoped request, start with its requested question rather than expanding into a full repository scan.

Trace each important edge to actual code. Imports alone do not prove a runtime call or data transfer. Label inference and uncertainty; do not invent architectural intent, risks, or future work to fill a field.

## Build a tree of explanations

Each perspective is a top-level element. An element with meaningful internal structure is a group; one without useful further decomposition is a leaf. For each semantic node in a diagram:

1. Read the implementation it represents and record its role and `sources`.
2. Create a child directory whose name matches the TikZ node ID, with `description.md` and `meta.yaml`. Every node gets a description — no exceptions.
3. If distinct responsibilities or interactions need explaining, make it a group with its own diagram and repeat. Otherwise stop at the leaf.

Do not recurse just because a directory has subdirectories. Stop at trivial wrappers, external systems, or a cohesive unit whose internals do not answer the perspective's question. A node may cover several small, cohesive files when they play one role for this question. Keep each diagram at one useful abstraction level, about twelve semantic nodes at most. If it becomes crowded, extract detail into a child, or move externals into an `external-integrations` perspective, instead of shrinking all text.

The containment tree must be acyclic. Real feedback loops and cyclic dependencies may still appear as labeled edges. When the same component appears in several perspectives, give each appearance the same `sources` and connect them through `refs` rather than nesting it indefinitely. Layout coordinates, edge labels, legends, and decorative frames are not semantic nodes: give them no ID or an ID starting with `_`.

## Write the files

Follow [format.md](references/format.md) for the layout, `meta.yaml`, and the navigation contract. In brief:

- `index.md`: scope, analyzed commit and working-tree caveat, language, selected perspectives with relative links, and render status.
- `description.md`: parent link first; role, boundary, source links with relevant symbols, and evidence for relationships. Groups embed `diagram.svg`, link the editable `diagram.tikz`, and link each child description. Link the optional fields that exist.
- `meta.yaml`: `kind`, `status`, `sources`, `children`, `refs`, `analyzed_commit`, `working_tree_dirty`, and for groups `render`.
- Optional fields (`context`, `constraint`, `concern`, `todo`, `note`) only when evidenced.

Start each diagram from [architecture.tikz](assets/architecture.tikz), replacing all example nodes and labels. Use the `entry`, `store`, `external`, and `concern` styles for those roles, and `context` for outside components a drill-down talks to. Label every edge with the relationship or data exchanged. Put a readable name and a short source path in each node; keep long paths and explanation in descriptions.

## Refresh existing documentation

Read `config.yaml` and reuse its language. Run:

```sh
uv run <skill>/scripts/omtkc.py stale .omtkc
```

`STALE` lines name elements whose recorded sources changed since their `analyzed_commit`; `NEW` lines name changed or untracked files no element covers; `UNKNOWN` means no baseline. Reread those sources, plus callers, callees, entry points, and configuration they touch, and decide which elements, parent diagrams, and perspectives change. Without a trustworthy baseline, inspect current source rather than claiming a complete incremental scan.

Preserve `note.md`, other human-written text, stable IDs, and unaffected subtrees. Update related descriptions, diagrams, `meta.yaml`, navigation, and renders together. Set `analyzed_commit` to the HEAD you diffed against only on elements whose changed or newly added sources you checked against their description and diagram; a wording fix alone does not move it. A source whose diff is irrelevant to the element (a version bump, or a change outside the symbol named after `#`) still counts as checked: move the commit without editing the description. `stale` reports a new file as `NEW` when no leaf covers it: assign it to an existing leaf or add one. When a new node would push a diagram past about twelve nodes, fold it into an existing node or draw it in another perspective, and say so in the description. In `index.md`, state the refresh commit and that elements carry their own `analyzed_commit` (`omtkc.py tree` shows them).

While refreshing an element, bring it up to the current format: narrow broad `sources` (they hide `NEW` files), and replace a re-rendered diagram's option block with the current template's. If `check` reports breakage that predates your change, fix it; when a link points to a missing human-written file, remove the link and mention it in your report instead of creating an empty file. For removed components follow the retirement rule in format.md; do not delete human-authored material silently. Never claim unchanged diagrams were revalidated unless they were. A newer tikzc alone does not require re-rendering unchanged diagrams; if you do re-render them, inspect and `stamp` them so `render.tikzc_version` stays truthful.

## Validate and deliver

For each new or changed diagram, run `tikzc check`, render SVG and PNG, and inspect the PNG with the available image-reading tool, following [rendering.md](references/rendering.md). Repair and repeat. Then record the result with `uv run <skill>/scripts/omtkc.py stamp <group-dir> --check pass --visual inspected` (or `fail` / `pending`), which writes the `render` block of `meta.yaml`.

Run the structural check and fix every error:

```sh
uv run <skill>/scripts/omtkc.py check .omtkc
uv run <skill>/scripts/omtkc.py tree .omtkc
```

The checker covers IDs, directories, links, sources, and render freshness; it cannot judge whether an arrow is true. Confirm important arrows against the implementation yourself.

Report the root index path, perspectives and meaningful drill-downs, the checker result, rendering results and tikzc version, any `visual: pending` diagrams, and unresolved questions. Suggest committing `.omtkc/` so future refreshes have a baseline. The deliverable is local files; this workflow does not publish, upload, or perform Git mutations.
