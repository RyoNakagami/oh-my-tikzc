# Rendering with native tikzc

The supported renderer is [RyoNakagami/tikzc](https://github.com/RyoNakagami/tikzc), a Rust-native renderer for a practical subset of TikZ. tikzc 1.2.0 or later is required; earlier releases, including the pre-1.0 TypeScript/TeX workflow, are not supported. The bundled starter is verified with tikzc 1.2.0 and 1.2.1. Check the installed executable rather than assuming an older workflow. Syntax beyond the starter must be checked against the executable in use.

## Authoring

Start with the bundled `../assets/architecture.tikz`. Use a bare `tikzpicture`; no LaTeX document wrapper or TeX subprocess is needed. For Japanese labels, the starter selects bundled `IPAexGothic` through `#| mainfont: IPAexGothic`. Do not require system font installation for this default.

Prefer named nodes, explicit positions or simple relative positioning, straight/orthogonal paths, and modest styles. Native tikzc supports a subset, not arbitrary PGF/TikZ. The [native compatibility contract](https://github.com/RyoNakagami/tikzc/blob/main/docs/RUST_ENGINE.md) and the installed CLI's diagnostics take precedence over general TikZ examples. Consult that contract when a feature is needed; do not load its entire catalog for a simple diagram.

Use explicit `\\` line breaks for predictable labels and escape TeX-sensitive characters in source paths, such as `\_` for underscores and `\#` for hashes. `--` becomes an en dash, so write CLI flags as `-{}-preview-server`, which works in every supported version (from 1.2.1, `\texttt{--x}` and `\verb|--x|` also keep both hyphens). Avoid `~` in labels (write "home" in words); `\textasciitilde` renders as a raised tilde. Keep important information in prose when a path would make a node too wide. Do not insert untrusted source text as executable TeX commands.

Arrange a flow left to right or a hierarchy top to bottom. Use consistent node styles and generous space for edge labels. Distinguish external systems with a dashed border and a label, not color alone. Do not enforce a slide aspect ratio unless the user is preparing slides. A header declaring width or height does not guarantee that standalone output has those pixel dimensions.

Keep the template's `#| mainfont: IPAexGothic` header for any language; it is the bundled font and also covers Latin text.

Edge labels are the most common layout defect. Prefer horizontal and vertical segments: place a label `above` a horizontal edge and `left`/`right` of a vertical one, and use the template's `rel` style so its white fill masks crossing lines. On `-|` and `|-` paths, `pos=0.25` is on the first segment and `pos=0.75` on the second. Avoid `sloped` labels on short diagonal edges, where they land on the target node. Draw two opposite edges between the same pair as parallel lines, for example `([yshift=3mm]a.east) -- ([yshift=3mm]b.west)` and the reverse with `-3mm`. Crossings are acceptable when they are unambiguous; otherwise reroute, or omit a secondary edge and list it in the description.

Constructs unsupported or misleading in tikzc 1.2.0 and fixed in 1.2.1: the `-Stealth` arrow option, `yshift` inside a `label={…}` option, `dash dot`, anchor names such as `north east` as a label position, `\verb`, and `double` on node borders (accepted but not drawn in 1.2.0). The template avoids all of them so it renders the same on both versions; use them only after checking `tikzc --version`. In 1.2.1 a `north east` label is placed like `45`, on the border, not at the node's corner; use an angle when the position matters.

## Compile, render, inspect

From the repository being documented, for each diagram:

```sh
tikzc check .omtkc/overall-architecture/diagram.tikz
tikzc .omtkc/overall-architecture/diagram.tikz -f both -o .omtkc/overall-architecture/
```

These commands generate `diagram.svg` and `diagram.png`. PNG resolution can be set with `--dpi`; it is not a requested fixed canvas width. Use the available image-reading tool to open the PNG. Check:

- Text fits the nodes and remains readable at the intended display size.
- Edge labels do not collide with nodes, other labels, or lines.
- Arrowheads, direction, branches, and any feedback loop convey the intended relationships.
- Borders and decorative groups do not hide content or imply false ownership.
- Crossings are distinguishable from intentional junctions; reroute ambiguous connections.
- All semantic nodes have descriptions and all important edges have source evidence.

Compiler success alone does not establish layout quality or architectural accuracy. If the source changes after inspection, regenerate and inspect again.

## Diagnostics and stale output

For unsupported syntax, use the source-position diagnostic to simplify the input without changing its meaning. There is no silent fallback to TeX or Mermaid. If a required concept cannot be represented, explain the limitation and leave the diagram explicitly incomplete. Avoid repeated identical retries; after a failed correction, reassess the construct or report the blocker.

A failed compile can leave an older render on disk. Do not treat that old image as the current result: record failed validation in the relevant description/index and say that any existing render is stale. For updates where preserving the last successful files matters, render into a temporary directory outside `.omtkc/` (for example under the system temp directory) first and replace the published local SVG/PNG only after successful generation and inspection.

If the image-reading tool is unavailable, say “compiled; visual inspection pending.” Do not replace actual inspection with a claim based on file existence.

## Viewing

Open the generated index and its relative Markdown links in a Markdown preview. The SVG is a static image and the PNG is a portable raster copy. Users who already have the tikzc VSCode extension can open the `.tikz` source in its preview. Do not install extensions or start servers simply to finish a scan.
