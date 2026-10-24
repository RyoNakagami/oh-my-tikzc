[← 描画エンジン](../description.md)

# ラベル SVG 共有

種別：リーフ．解析コミット `32ac110`．

Typst が出力したラベル SVG を図全体の SVG に埋め込む（[render/label_svg.rs](https://github.com/RyoNakagami/tikzc/blob/ef3a589541731a9c7098921c25f4770d86ac5d37/src/render/label_svg.rs)）．同じグリフの自己完結したシンボルは `<defs>` で共有し，それ以外の ID はラベルごとに名前空間を分けて衝突を防ぐ．グリフのパスは [render/glyph_path.rs](https://github.com/RyoNakagami/tikzc/blob/ef3a589541731a9c7098921c25f4770d86ac5d37/src/render/glyph_path.rs) の `round_path` で小数 4 桁に丸め，SVG を小さくする．`checkpoint` / `rollback` により，失敗した要素の定義を取り消せる．

## ソース

- [src/render/label_svg.rs](https://github.com/RyoNakagami/tikzc/blob/ef3a589541731a9c7098921c25f4770d86ac5d37/src/render/label_svg.rs)
- [src/render/glyph_path.rs](https://github.com/RyoNakagami/tikzc/blob/ef3a589541731a9c7098921c25f4770d86ac5d37/src/render/glyph_path.rs)
