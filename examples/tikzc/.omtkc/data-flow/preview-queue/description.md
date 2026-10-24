[← データフロー（VSCode プレビューと編集）](../description.md)

# 更新キュー

種別：リーフ．解析コミット `32ac110`．

編集のたびにコンパイルが積み上がらないようにする小さなキュー（[preview-queue.ts](https://github.com/RyoNakagami/tikzc/blob/ef3a589541731a9c7098921c25f4770d86ac5d37/vscode-extension/src/preview/preview-queue.ts)）．`update(value, delay)` は版番号を進めて待機中の要求を捨て，遅延後に最新の 1 件だけを `compile` に渡す．同時に走るジョブは 1 つで，結果やエラーは版番号が最新のときだけ `publish` / `fail` に渡す．古い結果がプレビューを上書きしないための仕組みである．

## ソース

- [vscode-extension/src/preview/preview-queue.ts](https://github.com/RyoNakagami/tikzc/blob/ef3a589541731a9c7098921c25f4770d86ac5d37/vscode-extension/src/preview/preview-queue.ts)
