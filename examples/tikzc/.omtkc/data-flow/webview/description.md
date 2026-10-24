[← データフロー（VSCode プレビューと編集）](../description.md)

# Webview

種別：リーフ．解析コミット `32ac110`．

プレビューパネル内のブラウザ側スクリプト（[native-preview.ts](https://github.com/RyoNakagami/tikzc/blob/ef3a589541731a9c7098921c25f4770d86ac5d37/vscode-extension/webview/native-preview.ts)，[native-selection.ts](https://github.com/RyoNakagami/tikzc/blob/ef3a589541731a9c7098921c25f4770d86ac5d37/vscode-extension/webview/native-selection.ts)）．受け取った SVG と PNG を Blob URL の `<img>` として表示し，文字を再計測・再配置しない（[docs/ARCHITRECTURE.md](https://github.com/RyoNakagami/tikzc/blob/ef3a589541731a9c7098921c25f4770d86ac5d37/docs/ARCHITRECTURE.md) Article 2）．`editing` メタデータを使って，ノードの当たり判定，パスの端点・中間点のハンドル，図形の追加，重なり順の変更，ズームとパンを提供する．操作はすべて `host.postMessage` でホストへ送り，ソースの書き換えはホスト側が行う．

## ソース

- [vscode-extension/webview/native-preview.ts](https://github.com/RyoNakagami/tikzc/blob/ef3a589541731a9c7098921c25f4770d86ac5d37/vscode-extension/webview/native-preview.ts)
- [vscode-extension/webview/native-selection.ts](https://github.com/RyoNakagami/tikzc/blob/ef3a589541731a9c7098921c25f4770d86ac5d37/vscode-extension/webview/native-selection.ts)
