[← データフロー（VSCode プレビューと編集）](../description.md)

# tikzc プレビューサーバ

種別：リーフ．解析コミット `32ac110`．

`tikzc --preview-server`（[src/main.rs](https://github.com/RyoNakagami/tikzc/blob/ef3a589541731a9c7098921c25f4770d86ac5d37/src/main.rs) の `preview_server`）．標準入力から 1 行ずつ JSON を読み，`render::compile_with_text` と `Diagram::png` で `{svg, png, editing}` か `{error}` を返す．ファイルは書かない．1 行は 16 MiB までで，超えるか改行で終わらなければ終了する．`TextEngine` をプロセス内で使い回す点が，毎回新しく作る CLI の `compile` との違いである．診断のファイル名は `document.tikz` 固定で，拡張側が行番号を補正する．

全体図では [CLI](../../overall-architecture/cli/description.md) の 1 モードとして描かれている．

## 他の視点での同じ要素

- [tikzc CLI](../../overall-architecture/cli/description.md)（`overall-architecture/cli`）

## ソース

- [src/main.rs — `preview_server`](https://github.com/RyoNakagami/tikzc/blob/ef3a589541731a9c7098921c25f4770d86ac5d37/src/main.rs)
