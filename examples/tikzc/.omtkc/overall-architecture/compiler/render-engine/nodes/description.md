[← 描画エンジン](../description.md)

# ノード配置

種別：リーフ．解析コミット `ef3a589`．

`\node` と `\matrix` の解析・配置（[src/render/nodes.rs](https://github.com/RyoNakagami/tikzc/blob/ef3a589541731a9c7098921c25f4770d86ac5d37/src/render/nodes.rs)）．

- `parse_node`：オプション，名前，`at` 位置，ラベルを読み，ラベルはテキストエンジンの `layout` で組版する．
- `place_node`：形状と `inner sep` / `outer sep` / `minimum width` から境界を決め，枠を `paint` で描き，ラベル SVG を `glyphs.embed` で埋め込む．キャンバス編集用にラベルの元ソース範囲・境界・フォントを記録する．
  - 枠が描かれる（`draw` がある）ノードでは `double_strokes` で二重線を 2 回描く（1.2.1，[塗り・線の属性](../paint/description.md)）．
  - `label={[...]pos:text}` の位置は角度・`above` 系に加え，1.2.1 から `north east` などのアンカー名も受け付ける（`north east` は `45` と同じ扱いで，枠上に置かれる）．ラベルの `xshift` / `yshift` は配置後の位置をずらす．回転などその他の変形はエラーのまま．
- `place_path_node`：パスの途中に書かれたノードを配置する（パス構築から呼ばれる）．
- `matrix`：`\matrix` をセル単位のノードに分解する．

## ソース

- [src/render/nodes.rs](https://github.com/RyoNakagami/tikzc/blob/ef3a589541731a9c7098921c25f4770d86ac5d37/src/render/nodes.rs)
