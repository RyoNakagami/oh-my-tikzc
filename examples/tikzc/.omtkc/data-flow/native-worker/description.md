[← データフロー（VSCode プレビューと編集）](../description.md)

# 常駐ワーカー

種別：リーフ．解析コミット `32ac110`．

`NativeWorker` クラス（[worker.ts](https://github.com/RyoNakagami/tikzc/blob/ef3a589541731a9c7098921c25f4770d86ac5d37/vscode-extension/src/preview/worker.ts)）．`spawn(binary, ["--preview-server"])` で起動した 1 つの `tikzc` プロセスを保持し，フォントとラベルのキャッシュを編集間で使い回す．同時に 1 件の要求しか受けず，`{source, dpi}` を 1 行の JSON で送り，改行までを 1 応答として読む．応答が 64 MiB を超える，60 秒で返らない，プロセスが終了する，のいずれかで失敗扱いにしてプロセスを止める．

## ソース

- [vscode-extension/src/preview/worker.ts](https://github.com/RyoNakagami/tikzc/blob/ef3a589541731a9c7098921c25f4770d86ac5d37/vscode-extension/src/preview/worker.ts)
