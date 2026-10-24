[← 描画エンジン](../description.md)

# パス構築

種別：リーフ．解析コミット `ef3a589`．

`\draw`，`\fill`，`\path`，`\clip`，`\shade` などのパスを組み立てる最大のモジュール（[render/paths.rs](https://github.com/RyoNakagami/tikzc/blob/ef3a589541731a9c7098921c25f4770d86ac5d37/src/render/paths.rs)）．

- `path`：`--`，`|-`，`-|`，`..controls..`，`to`，円・楕円・矩形・グリッド・`plot` などの操作を読み，SVG の `d` を作る．
- `arrow`：矢印先端を配置する．形状は [src/arrows.rs](https://github.com/RyoNakagami/tikzc/blob/ef3a589541731a9c7098921c25f4770d86ac5d37/src/arrows.rs)．曲線の計算は [src/curve.rs](https://github.com/RyoNakagami/tikzc/blob/ef3a589541731a9c7098921c25f4770d86ac5d37/src/curve.rs)．
- `double` 線は [塗り・線の属性](../paint/description.md) の `double_strokes` で外側と内側の 2 本を描く（1.2.1 でノードと共通化）．
- [src/arrows.rs](https://github.com/RyoNakagami/tikzc/blob/ef3a589541731a9c7098921c25f4770d86ac5d37/src/arrows.rs) の `is_spec` は，`-Stealth` のような裸の矢印指定かどうかを判定し，[オプション解決](../../option-resolver/description.md) から呼ばれる（1.2.1）．
- `brace`，`rounded_path`，`orthogonal_corner`：装飾と角丸．
- 編集用に端点・中間点の元ソース範囲を `path_handle` で記録する．

## ソース

- [src/render/paths.rs](https://github.com/RyoNakagami/tikzc/blob/ef3a589541731a9c7098921c25f4770d86ac5d37/src/render/paths.rs)
- [src/curve.rs](https://github.com/RyoNakagami/tikzc/blob/ef3a589541731a9c7098921c25f4770d86ac5d37/src/curve.rs)
- [src/arrows.rs](https://github.com/RyoNakagami/tikzc/blob/ef3a589541731a9c7098921c25f4770d86ac5d37/src/arrows.rs)
