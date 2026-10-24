[← コンパイラ（Rust ライブラリ）](../description.md)

# テキストエンジン

種別：リーフ．解析コミット `ef3a589`．

ノードのラベルを Typst で組版し，グリフをパスにした SVG と寸法（`Label`）を返す（[src/text.rs](https://github.com/RyoNakagami/tikzc/blob/ef3a589541731a9c7098921c25f4770d86ac5d37/src/text.rs)）．TeX の数式は `mitex::convert_math` で Typst の数式に変換する．

- `TextEngine::new()`：埋め込みフォントで `FontBook` を作る．
- `TextEngine::layout(text, options, styles, mainfont)`：組版の本体．同じ入力はキャッシュから返す（`cache_hits`）．長寿命のプレビューサーバ向けに，エントリ 256 件または合計 16 MiB を超えるとキャッシュを捨てる．
- `mainfont` が埋め込みフォントに無いときだけ，`fontdb::Database::load_system_fonts()` で OS のフォントを一度だけ探す．既定のフォントだけを使う図は決定的で，この走査を行わない（コード中のコメント）．
- 1.2.1 から `\verb|…|`（`\verb*` も）を等幅・合字なしの文字列として組む．また `\texttt{…}` と `\ttfamily` の中では `--` / `---` をダッシュに変換しない（`Converter::typewriter`，`\ttfamily` の効果は囲むグループの終わりで戻る）．
- 描画エンジンの [nodes](../render-engine/nodes/description.md) から呼ばれる．

## ソース

- [src/text.rs](https://github.com/RyoNakagami/tikzc/blob/ef3a589541731a9c7098921c25f4770d86ac5d37/src/text.rs)
