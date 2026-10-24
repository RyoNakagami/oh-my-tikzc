# はじめに：インストールと使い方

[English](../getting-started.md) · [仕組み](how-it-works.md)

このガイドでは，前提ツールのインストールから，自分のリポジトリの `.omtkc/` アーキテクチャドキュメントを生成してコミットするまでを順に説明する．最後に，コード変更後にドキュメントを最新に保つ方法も扱う．

## 1. 前提ツールのインストール

oh-my-tikzc は AI コーディングエージェント向けのスキルパッケージであり，次の 2 つのコマンドラインツールを使う．

| ツール | 用途 | バージョン |
| --- | --- | --- |
| [tikzc](https://github.com/RyoNakagami/tikzc#installation) | 各 `diagram.tikz` を SVG / PNG にコンパイルする | **1.2.0 以上** |
| [uv](https://docs.astral.sh/uv/getting-started/installation/) | 同梱チェッカー `omtkc.py` を実行し，PyYAML を取得する | 最近のリリースならよい |

両方が PATH 上にあることを確認する．

```sh
tikzc --version   # tikzc 1.2.1
uv --version
```

tikzc はフォントを内蔵したネイティブ描画エンジンなので，TeX のインストールは不要である．1.2.0 より前のリリース（旧 TypeScript/TeX パイプラインを含む）はサポートしない．

uv は必須ではない．uv がなければチェッカーは `python3`（3.10 以上）で動く．PyYAML があればそれを使い，なければ組み込みのパーサーで読む．

加えて，スキルを読み込めるエージェント（[Claude Code](https://code.claude.com/docs/en/skills) または [Codex](https://learn.chatgpt.com/docs/build-skills)）が必要である．

## 2. スキルのインストール

このリポジトリは，両ツールが読めるプラグインマーケットプレイスである．マーケットプレイスを追加し，`tikzc-architecture` スキルを含む `oh-my-tikzc` プラグインをインストールする．

**Claude Code**:

```sh
claude plugin marketplace add RyoNakagami/oh-my-tikzc
claude plugin install oh-my-tikzc@oh-my-tikzc
```

**Codex**:

```sh
codex plugin marketplace add RyoNakagami/oh-my-tikzc
codex plugin add oh-my-tikzc@oh-my-tikzc
```

インストール後は，ドキュメント化したいリポジトリで**エージェントのセッションを新しく開始する**．スキルはセッション開始時に読み込まれる．

### スキルの更新

```sh
# Claude Code
claude plugin marketplace update oh-my-tikzc
claude plugin update oh-my-tikzc@oh-my-tikzc

# Codex
codex plugin marketplace upgrade oh-my-tikzc
```

### 手動インストール

マーケットプレイスを使わない場合や，プロジェクト経由でスキルを共有する場合に使う．このリポジトリを clone またはダウンロードし，そのルートで以下のコマンドを実行する．`skills/tikzc-architecture/` ディレクトリは**丸ごと**コピーすること．`references/`，`assets/`，`scripts/`，`agents/` はすべて実行時に使われる．

**Claude Code**（個人スキル）:

```sh
mkdir -p "$HOME/.claude/skills"
test ! -e "$HOME/.claude/skills/tikzc-architecture" && test ! -L "$HOME/.claude/skills/tikzc-architecture" && cp -R skills/tikzc-architecture "$HOME/.claude/skills/"
```

**Codex**（個人スキル）:

```sh
mkdir -p "$HOME/.agents/skills"
test ! -e "$HOME/.agents/skills/tikzc-architecture" && test ! -L "$HOME/.agents/skills/tikzc-architecture" && cp -R skills/tikzc-architecture "$HOME/.agents/skills/"
```

`test` による確認は，同名のスキルがすでにインストールされているとコピーを止める．このため既存のインストールを誤って上書きすることはない．更新するときは，古いディレクトリを退避してから新しいものをコピーし，問題がなければ退避したものを消す．

**プロジェクト単位でインストールする場合**は，同じディレクトリを対象プロジェクトの `.claude/skills/`（Claude Code）または `.agents/skills/`（Codex）にコピーする．そのプロジェクトを clone した全員がスキルを使えるようになる．

**Windows** では，エクスプローラーや PowerShell で，ユーザープロファイルまたはプロジェクト配下の対応するフォルダにコピーする．

手動でインストールしたスキルにはプラグインの接頭辞が付かない．以下の `oh-my-tikzc:tikzc-architecture` の代わりに `/tikzc-architecture` または `$tikzc-architecture` で呼び出す．

## 3. 最初のアーキテクチャツリーを生成する

ドキュメント化したいリポジトリのルートでスキルを呼び出す．

Claude Code:

```text
/oh-my-tikzc:tikzc-architecture このリポジトリのアーキテクチャを日本語で説明して．
```

Codex:

```text
$oh-my-tikzc:tikzc-architecture このリポジトリのアーキテクチャを日本語で説明して．
```

「tikzc でこのコードベースを図解して」のような自然な依頼でも動く．依頼文の言語がドキュメントの言語になり（既定は英語），以後の更新のために `config.yaml` に保存される．日本語で書いてほしい場合は，そう依頼すればよい．

### 範囲を絞る

リポジトリ全体を走査する場合，最初のパースペクティブは必ず `overall-architecture` になる．大きなリポジトリの場合や，知りたい問いが 1 つに決まっている場合は，範囲を指定する．

```text
tikzc-architecture で src/api/ のリクエストライフサイクルだけをドキュメント化して．
tikzc-architecture で CLI コマンドのディスパッチだけを図にして．
出力先は .omtkc/ ではなく docs/architecture/ にして．
```

### エージェントが行うこと

実行中，エージェントは次のことを行う．

1. マニフェスト，エントリポイント，既存ドキュメントを読み，現在のコミットを記録する．
2. データフローやコマンドディスパッチなど，それぞれ異なる問いに答えるパースペクティブを選ぶ．
3. 説明文と `meta.yaml` を書き，内部構造をもつ部品には `diagram.tikz` も書く．
4. `tikzc check` を実行し，SVG / PNG を描画して，各 PNG を目視で確認する．
5. `omtkc.py check` を実行し，エラーをすべて直す．

最後に，ルートのインデックス，作成したパースペクティブ，描画とチェッカーの結果，未解決の疑問点を報告する．各ステップの詳細は[仕組み](how-it-works.md)で説明する．

## 4. 結果を読む

出力はリポジトリルートの `.omtkc/` に置かれる．

```text
.omtkc/
  config.yaml                  # スキーマ，言語，スコープ
  index.md                     # ここから読む
  overall-architecture/
    description.md             # 説明 + diagram.svg の埋め込み
    meta.yaml                  # sources，children，解析コミット，描画状態
    diagram.tikz               # 編集可能なソース
    diagram.svg / diagram.png  # tikzc による描画結果
    compiler/                  # 図のノード 1 つにつき 1 ディレクトリ
      description.md
      meta.yaml
      ...
```

`.omtkc/index.md` を Markdown プレビュー（VS Code，GitHub，GitLab など）で開き，リンクをたどって下へ進む．各グループのページには SVG が埋め込まれ，編集可能な `.tikz` ソースへのリンクと，図のノードごとのページへのリンクがある．どのページにも親へ戻るリンクがある．

SVG は静的な画像であり，図のノードをクリックしても何も起きない．移動は図の下のリンクで行う．実際の出力例として，tikzc 自身を解析した [examples/tikzc/.omtkc/index.md](../../examples/tikzc/.omtkc/index.md) を参照するとよい．

**内容はレビューすること．** エージェントは各エッジをコードまでたどり，推測にはその旨を明記する．それでも図が説明するのは読んだコードの範囲だけであり，検証済みの仕様ではない．気になる矢印は，各ページのソースリンクで実装と照らし合わせること．

## 5. コミットする

```sh
git add .omtkc
git commit -m "docs: add architecture documentation"
```

`.omtkc/` をコミットすると，図の変更履歴が通常の `git diff` で見えるようになり，次回の更新の基準にもなる．各要素には，解析した時点のコミットが記録されている．

## 6. 最新に保つ

コードが変わったら更新を依頼する．

```text
/oh-my-tikzc:tikzc-architecture 既存の .omtkc ドキュメントを更新して．
```

エージェントは `omtkc.py stale` を実行し，前回の解析以降にソースファイルが変わった要素と，どの要素にも含まれていない変更ファイルを見つける．そのソースだけを読み直し，影響を受けるページと図を更新する．人が書いた `note.md`，安定した ID，変更のないサブツリーは保持される．結果を再度コミットする．

## チェッカーを自分で実行する

チェッカーはエージェントが自動で実行するが，直接実行することもできる．CI に組み込む場合や，`.tikz` を手で編集した後などに使う．`<skill>` はインストールしたスキルのディレクトリである．たとえば `~/.claude/plugins/cache/oh-my-tikzc/oh-my-tikzc/<version>/skills/tikzc-architecture`（Codex では `~/.codex/plugins/cache/` 配下），手動インストールなら `~/.claude/skills/tikzc-architecture` となる．

```sh
uv run <skill>/scripts/omtkc.py check .omtkc   # 構造，リンク，sources，描画の鮮度
uv run <skill>/scripts/omtkc.py tree  .omtkc   # 階層，解析コミット，描画状態
uv run <skill>/scripts/omtkc.py stale .omtkc   # 各要素の解析以降に何が変わったか
```

uv がなければ `uv run` を `python3` に置き換える．`check` はエラーがあると 0 以外の終了コードを返すので，CI のゲートとして使える．

`diagram.tikz` を手で編集した場合は，再描画して描画状態を記録し直す．そうしないと `check` が画像を古いと報告する．

```sh
tikzc check .omtkc/overall-architecture/diagram.tikz
tikzc .omtkc/overall-architecture/diagram.tikz -f both -o .omtkc/overall-architecture/
uv run <skill>/scripts/omtkc.py stamp .omtkc/overall-architecture --check pass --visual inspected
```

## トラブルシューティング

| 症状 | 原因と対処 |
| --- | --- |
| スキルが候補に出ない，`/oh-my-tikzc:tikzc-architecture` が見つからない | インストール前にセッションを開始した．新しいセッションを開始し，`claude plugin list` または `codex plugin list` で `oh-my-tikzc` がインストール済みか確認する．手動インストールの場合は，`SKILL.md` だけでなくディレクトリ全体をコピーしたかも確認する． |
| エージェントが tikzc がない，または古いと言う | tikzc 1.2.0 以上をインストールする．エージェントはソフトウェアを勝手にインストールしない．コードの解析は続けられるが，描画できるようになるまで図は `check: fail` として記録される． |
| `ERROR <group>: diagram.tikz changed after the recorded render (stale SVG/PNG)` | `.tikz` を編集した後に再描画していない．上記の手順で再描画して `stamp` を実行する． |
| `tree` の出力に `visual=pending`，または `visual inspection pending` 警告 | エージェントに画像を読むツールがなく，PNG を誰も見ていない．自分で開いて確認し，`--visual inspected` で stamp する． |
| `NEW <file>: … not covered by any leaf` | どの要素の `sources` にも含まれないファイルが変更・追加された．更新を依頼するか，`config.yaml` に `scope:` を加えてテストやドキュメントを除外する． |
| `--flag` がエンダッシュで描画される | tikzc は TeX のリガチャに従う．`.tikz` では `-{}-flag` と書く．詳細は [rendering.md](../../skills/tikzc-architecture/references/rendering.md) を参照． |
