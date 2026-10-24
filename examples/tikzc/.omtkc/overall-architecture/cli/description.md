[← 全体アーキテクチャ](../description.md)

# tikzc CLI

種別：リーフ．解析コミット `32ac110`．

実行ファイル `tikzc` の入口．`main()` → `run()` が引数を解釈し，3 つのモードに分かれる（[src/main.rs](https://github.com/RyoNakagami/tikzc/blob/ef3a589541731a9c7098921c25f4770d86ac5d37/src/main.rs)）．

1. **変換**：`tikzc <file.tikz> [-o out] [-f svg|png|both] [--dpi N] [-q]`．出力先が無ければ入力と同じ場所に拡張子を変えて書く．出力が入力と同一なら終了コード 2 で拒否する．
2. **検査**：`tikzc check <file.tikz>` はコンパイルだけを行い，何も書かない．
3. **プレビューサーバ**：引数がちょうど `--preview-server` のとき `preview_server()` に入る．VSCode 拡張専用で，ファイルを書かない．`TextEngine` を使い回してフォントとラベルのキャッシュを再利用する．詳細は [data-flow/tikzc-preview-server](../../data-flow/tikzc-preview-server/description.md)．

終了コードは 1（ラスタライズ・書き込み失敗），2（使い方・入力エラー），3（コンパイル診断）に分かれる（[docs/RUST_ENGINE.md](https://github.com/RyoNakagami/tikzc/blob/ef3a589541731a9c7098921c25f4770d86ac5d37/docs/RUST_ENGINE.md)）．

既知の懸念は [concern.md](concern.md) を参照．

## 他の視点での同じ要素

- [tikzc プレビューサーバ](../../data-flow/tikzc-preview-server/description.md)（`data-flow/tikzc-preview-server`）

## ソース

- [src/main.rs](https://github.com/RyoNakagami/tikzc/blob/ef3a589541731a9c7098921c25f4770d86ac5d37/src/main.rs)

## 補足

- [懸念](concern.md)
