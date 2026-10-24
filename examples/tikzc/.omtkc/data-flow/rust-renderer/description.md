[← データフロー（VSCode プレビューと編集）](../description.md)

# Rust レンダラ呼び出し

種別：リーフ．解析コミット `32ac110`．

`RustRenderer` クラス（[renderer.ts](https://github.com/RyoNakagami/tikzc/blob/ef3a589541731a9c7098921c25f4770d86ac5d37/vscode-extension/src/preview/renderer.ts)）．

- 要求を JSON 文字列をキーに最大 8 件キャッシュする．編集候補の検証で作った成果物は，その後の通常プレビューでも再利用される．
- 初回やバイナリ変更時に `tikzc --version` を実行し，`tikzc` でなければ拒否，1.0.0 未満も拒否，拡張とメジャー・マイナーが違えば一度だけ警告する．
- 設定の `mainfont` などを `#|` ヘッダとしてソースの前に付け（`prepareSource`），結果の編集メタデータのバイト位置と診断の行番号からその分を差し引く（[source-offsets.ts](https://github.com/RyoNakagami/tikzc/blob/ef3a589541731a9c7098921c25f4770d86ac5d37/vscode-extension/src/preview/source-offsets.ts)）．
- 60 秒使われなければ常駐ワーカーを止める．

## ソース

- [vscode-extension/src/preview/renderer.ts](https://github.com/RyoNakagami/tikzc/blob/ef3a589541731a9c7098921c25f4770d86ac5d37/vscode-extension/src/preview/renderer.ts)
- [vscode-extension/src/preview/source-offsets.ts](https://github.com/RyoNakagami/tikzc/blob/ef3a589541731a9c7098921c25f4770d86ac5d37/vscode-extension/src/preview/source-offsets.ts)
