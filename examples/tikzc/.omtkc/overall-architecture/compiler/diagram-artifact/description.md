[← コンパイラ（Rust ライブラリ）](../description.md)

# Diagram 成果物

種別：リーフ．解析コミット `32ac110`．

コンパイル結果の公開型 `Diagram`（[src/render/diagram.rs](https://github.com/RyoNakagami/tikzc/blob/ef3a589541731a9c7098921c25f4770d86ac5d37/src/render/diagram.rs)）．

- `svg`，`width`，`height`：SVG 文字列と pt 単位の寸法．`viewBox` は境界箱に約 2pt の余白を足したもの．
- `nodes`，`labels`：名前付きノードとラベルの原文．
- `editing`：VSCode のキャンバス編集用 JSON（`viewBox`，`nodes`，`objects`，`anchors`，`layers`，`insertionOffset`）．
- `png(dpi)`：SVG を `resvg` で白背景にラスタライズする．1 億画素または 1 辺 32768px を超えるとエラー．

CLI とプレビューサーバは同じ `png()` を使うため，プレビューとエクスポートは同じ成果物になる（[docs/ARCHITRECTURE.md](https://github.com/RyoNakagami/tikzc/blob/ef3a589541731a9c7098921c25f4770d86ac5d37/docs/ARCHITRECTURE.md) Article 2）．

## ソース

- [src/render/diagram.rs](https://github.com/RyoNakagami/tikzc/blob/ef3a589541731a9c7098921c25f4770d86ac5d37/src/render/diagram.rs)
- [src/render.rs — `compile_with_text`](https://github.com/RyoNakagami/tikzc/blob/ef3a589541731a9c7098921c25f4770d86ac5d37/src/render.rs)
