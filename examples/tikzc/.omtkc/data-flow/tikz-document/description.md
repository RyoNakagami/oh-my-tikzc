[← データフロー（VSCode プレビューと編集）](../description.md)

# .tikz ドキュメント

種別：リーフ．解析コミット `32ac110`．

VSCode の `TextDocument`．言語 ID が `tikz` か，ファイル名が `.tikz` で終わるものを対象にする（`isTikz`，[preview.ts](https://github.com/RyoNakagami/tikzc/blob/ef3a589541731a9c7098921c25f4770d86ac5d37/vscode-extension/src/preview/preview.ts)）．プレビューは保存前のバッファ内容（`doc.getText()`）を描くので，ディスク上のファイルとは一致しないことがある．キャンバス編集はこのバッファに 1 回の取り消し可能な `WorkspaceEdit` として反映される．

## 他の視点での同じ要素

- [TikZ ソース](../../overall-architecture/tikz-source/description.md)（`overall-architecture/tikz-source`）

## ソース

- [vscode-extension/src/preview/preview.ts — `request`](https://github.com/RyoNakagami/tikzc/blob/ef3a589541731a9c7098921c25f4770d86ac5d37/vscode-extension/src/preview/preview.ts)
