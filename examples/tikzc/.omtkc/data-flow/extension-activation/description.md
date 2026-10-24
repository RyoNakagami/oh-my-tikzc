[← データフロー（VSCode プレビューと編集）](../description.md)

# 拡張の起動

種別：リーフ．解析コミット `ef3a589`．

拡張の入口．`activate()` は `activateNativePreview(context)` を呼ぶだけで，`deactivate()` は空（[extension.ts](https://github.com/RyoNakagami/tikzc/blob/ef3a589541731a9c7098921c25f4770d86ac5d37/vscode-extension/src/extension.ts)）．コマンド `tikzc.showPreview`（Ctrl+K V），`tikzc.export` と設定 `tikzc.nativePath`，`tikzc.pngDpi`，`tikzc.debounceMs`，`tikzc.language` などは [package.json](https://github.com/RyoNakagami/tikzc/blob/ef3a589541731a9c7098921c25f4770d86ac5d37/vscode-extension/package.json) で宣言される．

## ソース

- [vscode-extension/src/extension.ts](https://github.com/RyoNakagami/tikzc/blob/ef3a589541731a9c7098921c25f4770d86ac5d37/vscode-extension/src/extension.ts)
- [vscode-extension/package.json](https://github.com/RyoNakagami/tikzc/blob/ef3a589541731a9c7098921c25f4770d86ac5d37/vscode-extension/package.json)
