[← 全体アーキテクチャ](../description.md)

# VSCode 拡張

種別：リーフ．解析コミット `ef3a589`．

`RyoNak.tikzc-preview`（表示名 TikZc Editor）．`.tikz` のプレビュー，キャンバス上での編集，SVG / PNG エクスポートを提供する．
描画は自前で行わず，マシンにインストールされた `tikzc`（PATH または設定 `tikzc.nativePath`）を `--preview-server` で起動して任せる．VSIX に実行ファイルは含まれない（[vscode-extension/README.md](https://github.com/RyoNakagami/tikzc/blob/ef3a589541731a9c7098921c25f4770d86ac5d37/vscode-extension/README.md)，[docs/ARCHITRECTURE.md](https://github.com/RyoNakagami/tikzc/blob/ef3a589541731a9c7098921c25f4770d86ac5d37/docs/ARCHITRECTURE.md) Article 2）．

コマンドは `tikzc.showPreview` と `tikzc.export` の 2 つ（[package.json](https://github.com/RyoNakagami/tikzc/blob/ef3a589541731a9c7098921c25f4770d86ac5d37/vscode-extension/package.json)）．

この要素の内部は「データがどう流れるか」という別の問いとして [data-flow 視点](../../data-flow/description.md) で分解している．全体図では 1 つの箱にとどめる．

## 他の視点での同じ要素

- [データフロー（VSCode プレビューと編集）](../../data-flow/description.md)（`data-flow`）

## ソース

- [vscode-extension/src/](https://github.com/RyoNakagami/tikzc/tree/ef3a589541731a9c7098921c25f4770d86ac5d37/vscode-extension/src)
- [vscode-extension/webview/](https://github.com/RyoNakagami/tikzc/tree/ef3a589541731a9c7098921c25f4770d86ac5d37/vscode-extension/webview)
- [vscode-extension/package.json](https://github.com/RyoNakagami/tikzc/blob/ef3a589541731a9c7098921c25f4770d86ac5d37/vscode-extension/package.json)
