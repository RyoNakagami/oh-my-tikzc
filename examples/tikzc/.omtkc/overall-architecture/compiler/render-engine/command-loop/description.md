[← 描画エンジン](../description.md)

# コマンドループ

種別：リーフ．解析コミット `32ac110`．

`compile_with_text` の本体（[src/render.rs](https://github.com/RyoNakagami/tikzc/blob/ef3a589541731a9c7098921c25f4770d86ac5d37/src/render.rs)）．

1. 先頭の `#|` ヘッダを読む．`filename` / `width` / `height` は無視，`mainfont` と `scale` を設定，`libraries` と `packages` は許可リスト（`arrows.meta`，`positioning`，`calc` など / `amsmath`，`amssymb`，`fontawesome`）以外を拒否する．
2. マクロ展開の結果を `Cursor` で読み，`\begin` / `\end`（`tikzpicture`，`scope`，`pgfonlayer` のみ），`\definecolor`，`\tikzset`，`\pgfdeclarelayer`，`\pgfsetlayers`，`\matrix`，`\node`，`\coordinate`，`\pgfmathsetseed`，各種パスコマンドを振り分ける．それ以外は `Unsupported syntax` の診断になる．
3. スコープごとに `State`（オプション，スタイル，クリップ，レイヤー）をスタックに積み，`\end` で戻す．
4. 全要素をレイヤー順に並べ，`<defs>` とグリフ定義を前に置いて SVG を組み立てる．寸法が 1e7pt を超えると拒否する．
5. 各ノードの 9 アンカー座標と編集メタデータを `Diagram.editing` に入れる．

## ソース

- [src/render.rs — `compile_with_text`](https://github.com/RyoNakagami/tikzc/blob/ef3a589541731a9c7098921c25f4770d86ac5d37/src/render.rs)
