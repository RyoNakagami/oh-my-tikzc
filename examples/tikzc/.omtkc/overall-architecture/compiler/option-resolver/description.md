[← コンパイラ（Rust ライブラリ）](../description.md)

# オプション解決

種別：リーフ．解析コミット `ef3a589`．

`[draw=blue, minimum width=3cm, ...]` のようなオプション文字列を検証し，スタイル（`/.style`）を展開して `Values`（キーと値の表）にする（[src/options.rs](https://github.com/RyoNakagami/tikzc/blob/ef3a589541731a9c7098921c25f4770d86ac5d37/src/options.rs)）．

- `Styles::resolve(input, base)`：スタイルとキーを解決する．未対応のキーや値はエラー文字列になり，描画エンジンが位置付きの診断へ変換する（`option_error`，`locate_options`）．
- 1.2.1 から，`dashdotted` などの別名を `dash dot` 系の正式名へ読み替え，`-Stealth` や `Latex-{Stealth[open]}` のような裸の矢印指定を `arrows` キーとして受け付ける．後者の判定は `crate::arrows::is_spec`（[src/arrows.rs](https://github.com/RyoNakagami/tikzc/blob/ef3a589541731a9c7098921c25f4770d86ac5d37/src/arrows.rs)，[パス構築](../render-engine/paths/description.md) の一部）を呼ぶ．
- `Styles::define_color`：`\definecolor` を登録する．
- `length` / `dim` / `number`：単位付き長さを pt に換算する．式部分は数式評価器が評価する．

## ソース

- [src/options.rs](https://github.com/RyoNakagami/tikzc/blob/ef3a589541731a9c7098921c25f4770d86ac5d37/src/options.rs)
