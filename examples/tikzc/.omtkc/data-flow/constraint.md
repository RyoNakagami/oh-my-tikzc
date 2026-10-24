# 不変条件：データフロー

[← データフロー](description.md)

| 制約 | 根拠 |
| --- | --- |
| キャンバス編集は候補ソースのコンパイルが成功したときだけ適用する | [preview.ts](https://github.com/RyoNakagami/tikzc/blob/ef3a589541731a9c7098921c25f4770d86ac5d37/vscode-extension/src/preview/preview.ts) `applyCanvasEdit` |
| 古い描画結果・古い操作は捨てる（版番号 `revision`，`renderToken`，本文の一致確認） | [preview-queue.ts](https://github.com/RyoNakagami/tikzc/blob/ef3a589541731a9c7098921c25f4770d86ac5d37/vscode-extension/src/preview/preview-queue.ts)，`applyCanvasEdit` |
| ワーカーへの同時要求は 1 件，応答は 64 MiB 以下，60 秒でタイムアウト | [worker.ts](https://github.com/RyoNakagami/tikzc/blob/ef3a589541731a9c7098921c25f4770d86ac5d37/vscode-extension/src/preview/worker.ts) |
| ワーカーは 60 秒使われないと停止 | [renderer.ts](https://github.com/RyoNakagami/tikzc/blob/ef3a589541731a9c7098921c25f4770d86ac5d37/vscode-extension/src/preview/renderer.ts) `renderFresh` |
| 1.0.0 未満の `tikzc` と，`tikzc` 以外の実行ファイルは拒否 | 同上 |
| 描画結果のキャッシュは 8 件 | `RustRenderer.render` |
| 設定値に改行を含めない（ヘッダ注入の防止） | `prepareSource` |
