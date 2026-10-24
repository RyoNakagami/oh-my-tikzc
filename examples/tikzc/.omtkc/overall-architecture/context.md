# 設計の背景：全体アーキテクチャ

[← 全体アーキテクチャ](description.md)

[docs/ARCHITRECTURE.md](https://github.com/RyoNakagami/tikzc/blob/ef3a589541731a9c7098921c25f4770d86ac5d37/docs/ARCHITRECTURE.md) が「非交渉の設計原則」として 4 条を定めており，構成はそれに沿っている．

- **Article 1**：サポート範囲は [docs/RUST_ENGINE.md](https://github.com/RyoNakagami/tikzc/blob/ef3a589541731a9c7098921c25f4770d86ac5d37/docs/RUST_ENGINE.md) とテストで固定された TikZ のサブセットであり，任意の TeX 実行や lualatex とのピクセル一致は約束しない．
- **Article 2**：レンダラは Rust エンジン 1 つだけ．CLI・プレビュー・エクスポートが同じ成果物を共有し，PNG は同じ SVG から作る．Webview は文字を再レイアウトしない．
- **Article 3**：実行時に TeX Live，Node.js，ネットワークを使わない．フォントは実行ファイルに埋め込む．
- **Article 4**：フォールバックレンダラは無い．未対応の入力は位置付き診断になり，失敗した実行は既存の出力を置き換えない．キャンバス編集は適用前にコンパイルで検証する．

同文書によれば，1.0.0 で TypeScript / LuaLaTeX 版 CLI とベンダリングした WYSIWYG エディタが削除された．README のアンインストール手順に旧 npm CLI の記述が残るのはその名残である．
