[← データフロー（VSCode プレビューと編集）](../description.md)

# エクスポート先

種別：リーフ．解析コミット `32ac110`．

エクスポートで書く SVG / PNG．既定の保存先は，ファイルを含むワークスペースのルート（無ければ最初のワークスペース，それも無ければファイルと同じフォルダ）に `<名前>.svg|png`（`exportUri`，[preview.ts](https://github.com/RyoNakagami/tikzc/blob/ef3a589541731a9c7098921c25f4770d86ac5d37/vscode-extension/src/preview/preview.ts)）．プレビューと同じレンダラ呼び出しを通るため，表示中のものと同じバイト列が書かれる．

## 他の視点での同じ要素

- [SVG / PNG ファイル](../../overall-architecture/output-files/description.md)（`overall-architecture/output-files`）

## ソース

- [vscode-extension/src/preview/preview.ts — `exportAs`](https://github.com/RyoNakagami/tikzc/blob/ef3a589541731a9c7098921c25f4770d86ac5d37/vscode-extension/src/preview/preview.ts)
