[← 全体アーキテクチャ](../description.md)

# TikZ ソース

種別：リーフ．解析コミット `32ac110`．

利用者が書く `.tikz` ファイル．リポジトリの外にある入力なので，図では破線（external）で示す．
`#|` で始まる先頭行はヘッダで，`mainfont`，`scale`，`libraries`，`packages` などを指定できる（解釈は [render-engine/command-loop](../compiler/render-engine/command-loop/description.md)）．

- CLI は `run()` で 1 ファイルだけを読む（[src/main.rs](https://github.com/RyoNakagami/tikzc/blob/ef3a589541731a9c7098921c25f4770d86ac5d37/src/main.rs)）．
- 拡張はディスクではなくエディタのバッファを読む（[data-flow/tikz-document](../../data-flow/tikz-document/description.md)）．
- 動作する例は [notebook/native-subset.tikz](https://github.com/RyoNakagami/tikzc/blob/ef3a589541731a9c7098921c25f4770d86ac5d37/notebook/native-subset.tikz)．サポート範囲は [docs/RUST_ENGINE.md](https://github.com/RyoNakagami/tikzc/blob/ef3a589541731a9c7098921c25f4770d86ac5d37/docs/RUST_ENGINE.md) とテストで決まる．

## 他の視点での同じ要素

- [.tikz ドキュメント](../../data-flow/tikz-document/description.md)（`data-flow/tikz-document`）

## ソース

- [src/main.rs — `run`](https://github.com/RyoNakagami/tikzc/blob/ef3a589541731a9c7098921c25f4770d86ac5d37/src/main.rs)
- [notebook/native-subset.tikz](https://github.com/RyoNakagami/tikzc/blob/ef3a589541731a9c7098921c25f4770d86ac5d37/notebook/native-subset.tikz)
