[← 全体アーキテクチャ](../description.md)

# SVG / PNG ファイル

種別：リーフ．解析コミット `32ac110`．

変換結果のファイル．SVG はグリフをパスとして含むため，閲覧側にフォントは不要である．PNG は同じ SVG を resvg でラスタライズしたもので背景は白（[src/render/diagram.rs](https://github.com/RyoNakagami/tikzc/blob/ef3a589541731a9c7098921c25f4770d86ac5d37/src/render/diagram.rs)，[docs/RUST_ENGINE.md](https://github.com/RyoNakagami/tikzc/blob/ef3a589541731a9c7098921c25f4770d86ac5d37/docs/RUST_ENGINE.md)）．

- CLI：`-f both -o dir/` のとき `dir/<入力名>.svg` と `.png` を書く．親ディレクトリは `create_dir_all` で作る（[src/main.rs](https://github.com/RyoNakagami/tikzc/blob/ef3a589541731a9c7098921c25f4770d86ac5d37/src/main.rs)）．
- 拡張：`exportAs()` が保存ダイアログで選んだ先へ書く（[preview.ts](https://github.com/RyoNakagami/tikzc/blob/ef3a589541731a9c7098921c25f4770d86ac5d37/vscode-extension/src/preview/preview.ts)）．

## 他の視点での同じ要素

- [エクスポート先](../../data-flow/export-files/description.md)（`data-flow/export-files`）

## ソース

- [src/main.rs — `run`](https://github.com/RyoNakagami/tikzc/blob/ef3a589541731a9c7098921c25f4770d86ac5d37/src/main.rs)
- [vscode-extension/src/preview/preview.ts — `exportAs`](https://github.com/RyoNakagami/tikzc/blob/ef3a589541731a9c7098921c25f4770d86ac5d37/vscode-extension/src/preview/preview.ts)
