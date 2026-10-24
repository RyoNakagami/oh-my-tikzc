# tikzc アーキテクチャ

このディレクトリは，リポジトリ [tikzc](https://github.com/RyoNakagami/tikzc) の構造を図と説明で辿れるようにしたドキュメントである．図は TikZ で書き，tikzc 自身で SVG / PNG に変換した．

> これは oh-my-tikzc の出力例で，tikzc の [`ef3a589`](https://github.com/RyoNakagami/tikzc/tree/ef3a589541731a9c7098921c25f4770d86ac5d37)（v1.2.1）時点の固定コピーである．ソースへのリンクはこのコミットのパーマリンクで，tikzc のその後の変更は反映されない．

## 範囲

- 対象：リポジトリ全体（Rust の CLI・コンパイラ `src/` と VSCode 拡張 `vscode-extension/`）．
- 除外：生成物（`target/`，`vscode-extension/dist/`，`node_modules/`），フォントの中身，テストのフィクスチャと画像ベースライン．`tests/`，`devtools/`，`.github/`，`notebook/` は実行時の構成要素ではないため図には入れていない．
- 解析したコミット：初回は `32ac110`，`ef3a589`（tikzc v1.2.1）で更新した．各要素は自分の `analyzed_commit` を持つ（`omtkc.py tree` で確認できる）．v1.2.1 で変更されたソースを含む要素だけを読み直して `ef3a589` に進め，それ以外は `32ac110` のままである．どちらの解析時も作業ツリーは `.omtkc/` 以外クリーンで，未コミットの変更は含まない．
- 言語：日本語（`config.yaml` の `language: ja`）．

## 視点

1. [全体アーキテクチャ](overall-architecture/description.md)：どの部品があり，どこからどこへ何が渡るか．
   - 掘り下げ：[コンパイラ](overall-architecture/compiler/description.md) → [描画エンジン](overall-architecture/compiler/render-engine/description.md)
2. [データフロー（VSCode プレビューと編集）](data-flow/description.md)：VSCode 上でソース・SVG / PNG・編集メタデータがどう流れ，どこへ書かれるか．

同じ部品が両方の視点に現れる場合（CLI とプレビューサーバ，出力ファイル，`.tikz` ソース，編集ハンドルとキャンバス編集）は，各説明の「他の視点での同じ要素」から相互に辿れる．

## 検証状況

- 図：4 枚（全体，コンパイラ，描画エンジン，データフロー）．すべて tikzc 1.2.1 の `tikzc check` に通り，SVG と PNG を再生成して PNG を目視確認した（1.2.0 時の出力と SVG はバイト単位で同一）．
- 構造：`omtkc.py check` でエラー 0（見本として切り出した後は `config.yaml` の `snapshot` により，ソースの存在確認を省いている）．
- 矢印は実装の呼び出し・データ受け渡しを読んで確認した．各説明の「関係の根拠」に該当箇所を記した．`import` だけを根拠にした矢印は無い．

## v1.2.1 での更新（`ef3a589`）

構成要素や矢印の追加・削除は無く，図の構造は変わっていない．機能追加は既存の要素の中に収まるため，説明だけを更新した．

- [オプション解決](overall-architecture/compiler/option-resolver/description.md)：`dash dot` 系の別名と裸の矢印指定（`-Stealth` など）．
- [塗り・線の属性](overall-architecture/compiler/render-engine/paint/description.md)：`dash dot` 系の破線と，ノード・パス共通の `double_strokes`．
- [ノード配置](overall-architecture/compiler/render-engine/nodes/description.md)：ノード枠の二重線，アンカー名と `xshift` / `yshift` によるラベル位置．
- [パス構築](overall-architecture/compiler/render-engine/paths/description.md)：二重線の共通化と `arrows::is_spec`．
- [テキストエンジン](overall-architecture/compiler/text-engine/description.md)：`\verb` と，等幅文字中の `--` の扱い．
- バージョン番号だけが変わった要素（全体アーキテクチャの `Cargo.toml`，VSCode 拡張と拡張の起動の `package.json`）と，`src/text.rs` のうち `TextEngine::new` が変わっていない埋め込みフォントは，読み直したうえで説明を変えずに `analyzed_commit` だけを進めた．

## 未解決の点

- CLI の `-f both` で PNG の書き込みが I/O エラーになった場合の挙動は，コードを読んだ結果であり実行では確かめていない（[懸念](overall-architecture/cli/concern.md)）．
