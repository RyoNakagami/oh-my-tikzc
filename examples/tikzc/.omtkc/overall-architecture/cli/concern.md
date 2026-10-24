# 懸念：tikzc CLI

[← tikzc CLI](description.md)

**`-f both` で書き込みが途中失敗すると，SVG だけが新しくなる可能性がある．**

[src/main.rs](https://github.com/RyoNakagami/tikzc/blob/ef3a589541731a9c7098921c25f4770d86ac5d37/src/main.rs) の `run()` は PNG への変換を書き込み前に済ませるが，書き込み自体は `for extension in formats` のループで SVG → PNG の順に `std::fs::write` する．PNG の書き込みが I/O エラー（容量不足や権限）で失敗した場合，SVG はすでに置き換わっている．[docs/ARCHITRECTURE.md](https://github.com/RyoNakagami/tikzc/blob/ef3a589541731a9c7098921c25f4770d86ac5d37/docs/ARCHITRECTURE.md) Article 4 の「失敗した実行は既存の出力を置き換えない」は，コンパイル失敗については守られているが，この書き込み失敗の場合は部分的にしか守られない．

これはコードから読み取った挙動であり，テストで再現は確認していない．影響は書き込み時の I/O エラーに限られる．
