[← 描画エンジン](../description.md)

# 塗り・線の属性

種別：リーフ．解析コミット `ef3a589`．

オプションから SVG の `stroke`，`fill`，線幅，破線パターン，不透明度，パターン塗りの属性を作る（[render/paint.rs](https://github.com/RyoNakagami/tikzc/blob/ef3a589541731a9c7098921c25f4770d86ac5d37/src/render/paint.rs)）．ノードの枠とパスの両方で使われる．

- 破線パターンは名前付きスタイルの表で決まる．1.2.1 で `dash dot`，`dash dot dot` とその `densely` / `loosely` 版が加わった（別名の読み替えは[オプション解決](../../option-resolver/description.md)）．
- `double_strokes`：`double` / `double distance` 指定を「外側の太い線」と「`double` 色で塗る隙間」の 2 回の描画に分ける．1.2.1 で [ノード配置](../nodes/description.md) と [パス構築](../paths/description.md) の共通処理として切り出され，線幅は `line_width` から取るため `thick` なども反映される．

## ソース

- [src/render/paint.rs](https://github.com/RyoNakagami/tikzc/blob/ef3a589541731a9c7098921c25f4770d86ac5d37/src/render/paint.rs)
