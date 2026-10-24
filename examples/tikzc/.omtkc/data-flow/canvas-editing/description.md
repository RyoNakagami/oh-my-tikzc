[← データフロー（VSCode プレビューと編集）](../description.md)

# キャンバス編集

種別：リーフ．解析コミット `32ac110`．

Webview の操作を元ソースへの差分 `SourceEdit {start, end, text}` に変換する純粋関数群（[editing.ts](https://github.com/RyoNakagami/tikzc/blob/ef3a589541731a9c7098921c25f4770d86ac5d37/vscode-extension/src/preview/editing.ts)）．`moveObject`，`movePathPoint`，`moveEndpoint`，`deleteObject`，`arrangeObject`，`insertDrawing`，`editNode`，`fontState` を公開する．位置はコンパイラが記録した元ソース範囲（[path-editing](../../overall-architecture/compiler/render-engine/path-editing/description.md)）に基づく．重なり順は `% tikzc layers begin` / `% tikzc order begin` で囲んだブロックとしてソースに書き込む．

## 他の視点での同じ要素

- [編集ハンドル](../../overall-architecture/compiler/render-engine/path-editing/description.md)（`overall-architecture/compiler/render-engine/path-editing`）

## ソース

- [vscode-extension/src/preview/editing.ts](https://github.com/RyoNakagami/tikzc/blob/ef3a589541731a9c7098921c25f4770d86ac5d37/vscode-extension/src/preview/editing.ts)
