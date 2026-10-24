[← コンパイラ（Rust ライブラリ）](../description.md)

# 公開 API

種別：リーフ．解析コミット `32ac110`．

クレートの外から見える入口．`tikzc::compile`，`tikzc::Diagram`，`tikzc::Diagnostic` を再公開し，`render`，`options`，`syntax`，`text` モジュールを `pub` にしている（[src/lib.rs](https://github.com/RyoNakagami/tikzc/blob/ef3a589541731a9c7098921c25f4770d86ac5d37/src/lib.rs)）．

- `compile(source)` は毎回新しい `TextEngine` を作って `compile_with_text` を呼ぶ（[src/render.rs](https://github.com/RyoNakagami/tikzc/blob/ef3a589541731a9c7098921c25f4770d86ac5d37/src/render.rs)）．CLI の変換・検査はこちらを使う．
- `render::compile_with_text(source, &mut engine)` はフォントとラベルのキャッシュを呼び出し側が持ち回すための入口で，プレビューサーバが使う．コメントによれば SVG 出力は変わらない．
- 利用例：[src/main.rs](https://github.com/RyoNakagami/tikzc/blob/ef3a589541731a9c7098921c25f4770d86ac5d37/src/main.rs)，ベンチマーク [examples/benchmark.rs](https://github.com/RyoNakagami/tikzc/blob/ef3a589541731a9c7098921c25f4770d86ac5d37/examples/benchmark.rs)．

## ソース

- [src/lib.rs](https://github.com/RyoNakagami/tikzc/blob/ef3a589541731a9c7098921c25f4770d86ac5d37/src/lib.rs)
- [src/render.rs — `compile`](https://github.com/RyoNakagami/tikzc/blob/ef3a589541731a9c7098921c25f4770d86ac5d37/src/render.rs)
