[← コンパイラ（Rust ライブラリ）](../description.md)

# 数式評価器

種別：リーフ．解析コミット `32ac110`．

PGF math 風の式を評価する（[src/expr.rs](https://github.com/RyoNakagami/tikzc/blob/ef3a589541731a9c7098921c25f4770d86ac5d37/src/expr.rs)）．`eval` は数値，`eval_value` は数値または文字列を返す．非有限値は `finite` で拒否する．`seed` は `rand` などの擬似乱数の種を管理し，`compile_with_text` の開始時に既定値へ戻されるため，同じ入力から同じ出力が得られる．

呼び出し元：マクロ展開器（`\pgfmathsetmacro` など），オプション解決（[src/options.rs](https://github.com/RyoNakagami/tikzc/blob/ef3a589541731a9c7098921c25f4770d86ac5d37/src/options.rs) の `length`），テキストエンジン（空白幅），描画エンジン（`\pgfmathsetseed`）．

## ソース

- [src/expr.rs](https://github.com/RyoNakagami/tikzc/blob/ef3a589541731a9c7098921c25f4770d86ac5d37/src/expr.rs)
