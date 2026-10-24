# 不変条件：全体アーキテクチャ

[← 全体アーキテクチャ](description.md)

コードで確認できる制約．

| 制約 | 根拠 |
| --- | --- |
| 変換結果をすべて作ってから出力を書く | [src/main.rs](https://github.com/RyoNakagami/tikzc/blob/ef3a589541731a9c7098921c25f4770d86ac5d37/src/main.rs) `run()` のコメント「Finish all conversions before writing any output.」 |
| 出力パスが入力と同じなら拒否（終了コード 2） | `run()` の `output must not overwrite input` |
| `#|` ヘッダは既知のキーだけ．`libraries` / `packages` は許可リスト | [src/render.rs](https://github.com/RyoNakagami/tikzc/blob/ef3a589541731a9c7098921c25f4770d86ac5d37/src/render.rs) `compile_with_text` |
| `scale` は (0, 100]，図の寸法は 1e7pt 以下 | 同上 |
| PNG は 1 億画素以下，1 辺 32768px 以下 | [src/render/diagram.rs](https://github.com/RyoNakagami/tikzc/blob/ef3a589541731a9c7098921c25f4770d86ac5d37/src/render/diagram.rs) `png` |
| マクロ展開は 2 MiB，200,000 ステップ，10,000 反復まで | [src/expand.rs](https://github.com/RyoNakagami/tikzc/blob/ef3a589541731a9c7098921c25f4770d86ac5d37/src/expand.rs) の定数 |
| プレビューサーバの 1 要求は 16 MiB まで | [src/main.rs](https://github.com/RyoNakagami/tikzc/blob/ef3a589541731a9c7098921c25f4770d86ac5d37/src/main.rs) `preview_server` |
| Webview は外部リソースを読まない（CSP `default-src 'none'`） | [preview-html.ts](https://github.com/RyoNakagami/tikzc/blob/ef3a589541731a9c7098921c25f4770d86ac5d37/vscode-extension/src/preview/preview-html.ts) |
