[← データフロー（VSCode プレビューと編集）](../description.md)

# プレビュー制御

種別：リーフ．解析コミット `32ac110`．

拡張の中心（[preview.ts](https://github.com/RyoNakagami/tikzc/blob/ef3a589541731a9c7098921c25f4770d86ac5d37/vscode-extension/src/preview/preview.ts) の `activateNativePreview`）．Webview パネル 1 つと対象ドキュメント 1 つを管理する．

- `request(doc)`：設定から `binary`（`tikzc.nativePath` か `tikzc`），`dpi`（既定 300），`mainfont`，追加パッケージ・ライブラリを集める．
- `refresh()`：`debounceMs`（既定 400ms）で更新キューに渡す．
- `publish()`：レンダラの結果を `render` メッセージで Webview に送る．同じ `id` が重複するノードは編集対象から外す．
- `applyCanvasEdit()`：Webview の操作を `SourceEdit` に変換し，候補ソースをコンパイルしてから適用する．`renderToken` と `document.getText()` を照合し，古い操作は捨てる．
- `exportAs()`：形式と保存先を選ばせ，ダイアログ表示前のスナップショットを描画して書き込む．
- パネル HTML は [preview-html.ts](https://github.com/RyoNakagami/tikzc/blob/ef3a589541731a9c7098921c25f4770d86ac5d37/vscode-extension/src/preview/preview-html.ts)（CSP で外部リソースを禁止），UI 文言の英日切り替えは [i18n.ts](https://github.com/RyoNakagami/tikzc/blob/ef3a589541731a9c7098921c25f4770d86ac5d37/vscode-extension/src/preview/i18n.ts)．

## ソース

- [vscode-extension/src/preview/preview.ts](https://github.com/RyoNakagami/tikzc/blob/ef3a589541731a9c7098921c25f4770d86ac5d37/vscode-extension/src/preview/preview.ts)
- [vscode-extension/src/preview/i18n.ts](https://github.com/RyoNakagami/tikzc/blob/ef3a589541731a9c7098921c25f4770d86ac5d37/vscode-extension/src/preview/i18n.ts)
- [vscode-extension/src/preview/preview-html.ts](https://github.com/RyoNakagami/tikzc/blob/ef3a589541731a9c7098921c25f4770d86ac5d37/vscode-extension/src/preview/preview-html.ts)
