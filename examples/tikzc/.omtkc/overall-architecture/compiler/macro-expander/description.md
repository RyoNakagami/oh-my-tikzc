[← コンパイラ（Rust ライブラリ）](../description.md)

# マクロ展開器

種別：リーフ．解析コミット `32ac110`．

TeX インタプリタではなく，上限付きのサブセット展開器（[src/expand.rs](https://github.com/RyoNakagami/tikzc/blob/ef3a589541731a9c7098921c25f4770d86ac5d37/src/expand.rs) 冒頭のドキュメントコメント）．出力の各バイトが元ソースの位置（`origins`）を保持し，生成されたマクロ本体は呼び出し位置を指す．これにより，展開後に起きたエラーでも元ソースの行・列で報告でき，VSCode のキャンバス編集も元ソースの範囲を書き換えられる．

- 入口：`pub fn expand(source) -> Result<Expanded, Diagnostic>`．
- 上限：`MAX_BYTES = 2 MiB`，`MAX_STEPS = 200_000`，`MAX_ITERATIONS = 10_000`．
- 条件分岐 `\ifnum`，`\ifodd`，`\ifdim` は展開時に決める．
- `\pgfmathsetmacro` などの式は数式評価器（`crate::expr::eval_value`）で評価し，`\pgfmathsetseed` で乱数種を設定する．
- 数値書式（`\pgfmathprintnumber`）は [src/expand/number.rs](https://github.com/RyoNakagami/tikzc/blob/ef3a589541731a9c7098921c25f4770d86ac5d37/src/expand/number.rs)．
- 字句処理の共通部品（`Cursor`，`clean`，`split_top`，`Diagnostic`）は [src/syntax.rs](https://github.com/RyoNakagami/tikzc/blob/ef3a589541731a9c7098921c25f4770d86ac5d37/src/syntax.rs)．

## ソース

- [src/expand.rs](https://github.com/RyoNakagami/tikzc/blob/ef3a589541731a9c7098921c25f4770d86ac5d37/src/expand.rs)
- [src/expand/number.rs](https://github.com/RyoNakagami/tikzc/blob/ef3a589541731a9c7098921c25f4770d86ac5d37/src/expand/number.rs)
- [src/syntax.rs](https://github.com/RyoNakagami/tikzc/blob/ef3a589541731a9c7098921c25f4770d86ac5d37/src/syntax.rs)
