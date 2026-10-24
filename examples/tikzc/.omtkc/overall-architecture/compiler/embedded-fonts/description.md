[← コンパイラ（Rust ライブラリ）](../description.md)

# 埋め込みフォント

種別：リーフ．解析コミット `ef3a589`．

実行ファイルに `include_bytes!` で埋め込まれるフォント（約 15 MiB）．IPAex 明朝・ゴシック，New Computer Modern Math，FontAwesome，Latin Modern Mono（通常・斜体）の 6 ファイル（[src/text.rs](https://github.com/RyoNakagami/tikzc/blob/ef3a589541731a9c7098921c25f4770d86ac5d37/src/text.rs)，[assets/fonts/README.md](https://github.com/RyoNakagami/tikzc/blob/ef3a589541731a9c7098921c25f4770d86ac5d37/assets/fonts/README.md)）．

実行時にファイルとして読むのではなく，ビルド時にバイナリへ取り込まれる．これがオフライン動作（[docs/ARCHITRECTURE.md](https://github.com/RyoNakagami/tikzc/blob/ef3a589541731a9c7098921c25f4770d86ac5d37/docs/ARCHITRECTURE.md) Article 3）を支える．既定の本文フォントは `IPAexMincho`（`compile_with_text` の初期値）で，`#| mainfont: IPAexGothic` で切り替えられる．

## ソース

- [assets/fonts/](https://github.com/RyoNakagami/tikzc/tree/ef3a589541731a9c7098921c25f4770d86ac5d37/assets/fonts)
- [src/text.rs — `TextEngine::new`](https://github.com/RyoNakagami/tikzc/blob/ef3a589541731a9c7098921c25f4770d86ac5d37/src/text.rs)
