# have-count-lean

Lean 4 の証明の中で `have` がどれだけ使われているかを数え、人間が書いた証明とAIが生成した証明を比べるスクリプトです。

Qiita の記事「**定理証明を自動で行う Neural Theorem Prover は、「タクティク記法」と「宣言的スタイル記法」のどちらで学習し、証明の答案を提出するのか**」の第９部「数で確かめる」で使用したものです。

- 記事：https://qiita.com/etale_cohomology/items/7f21731d0522935aa1af

## 必要なもの

Python 3.9 以上だけです。

追加のライブラリは不要です（`re`、`sys`、`pathlib`、`collections` のみ使用）。

**Lean や Mathlib をビルドする必要はありません。** ソースコードを文字列として読むだけです。

## データの取得

```bash
# Mathlib のソース（履歴とビルド済みファイルを落とさないので数百MBで済む）
git clone --depth 1 --filter=blob:none --sparse https://github.com/leanprover-community/mathlib4.git
cd mathlib4 && git sparse-checkout set Mathlib && cd ..

# DeepSeek-Prover-V2 が miniF2F を解いた証明（数MB）
git clone --depth 1 https://github.com/deepseek-ai/DeepSeek-Prover-V2.git
cd DeepSeek-Prover-V2 && unzip minif2f-solutions.zip -d sol && cd ..
```

## 実行

```bash
# 人間が書いた証明（Mathlib）を数える
python3 count_have.py mathlib4/Mathlib

# AIが生成した証明と比べる
python3 compare_generated.py
```

引数を省略した場合、`count_have.py` は `mathlib4/Mathlib` を、`compare_generated.py` は `DeepSeek-Prover-V2/sol` と `mathlib4/Mathlib` を見にいきます。

パスを変えたい場合は、引数で指定してください。

```bash
python3 compare_generated.py <生成証明のディレクトリ> <Mathlib のディレクトリ>
```

## 実行結果の例

記事で紹介した数値は、2026年11月時点の Mathlib の main ブランチ（ファイル8,705本、約237万行）で得たものです。

### count_have.py

```
定理・補題の数   : 192,515
have を含むもの  : 17,619 件 (9.2%)
１件あたり平均   : 0.19 個

--- 証明の長さ別 ---
  証明の長さ      定理の数   have を含む割合   １件あたりの have
  1行               15,150            0.0%             0.00
  2〜3行            99,270            0.4%             0.00
  4〜10行           62,438           12.2%             0.15
  11〜30行          13,860           57.4%             1.22
  31〜100行          1,750           92.0%             5.05
  101行以上             47          100.0%            16.57
```

### compare_generated.py

```
=== 全体の比較 ===
  生成（DeepSeek-Prover-V2）         438件   中央値   35行   have を含む  96.8%   １件平均 20.89個
  人間（Mathlib 全体）             192,515件   中央値    3行   have を含む   9.2%   １件平均  0.19個

=== 行数をそろえた比較 ===

【11〜30行】
  生成（DeepSeek-Prover-V2）         160件   中央値   22行   have を含む  98.8%   １件平均  5.92個
  人間（Mathlib）                 13,860件   中央値   15行   have を含む  57.4%   １件平均  1.22個

【31〜100行】
  生成（DeepSeek-Prover-V2）         176件   中央値   48行   have を含む  99.4%   １件平均 17.58個
  人間（Mathlib）                  1,750件   中央値   40行   have を含む  92.0%   １件平均  5.05個
```

Mathlib は日々更新されるため、別の時点で実行すれば数字は変わります。

再現したい場合は、取得したコミットを控えておくことをお勧めします。

## 集計方法の限界

このスクリプトは、Lean 4 の構文を正確に解析しているわけではありません。

行頭の字句を見る単純な方法で、おおよその傾向をつかむためのものです。

- `have` が文字列や識別子の一部として現れる場合も数えてしまいます
- 宣言の区切りの判定も粗いものです
- 比較したのは DeepSeek-Prover-V2 の1モデルだけで、他のモデルでは違う結果になる可能性があります

## ライセンス

MIT License

## 作者

Etale Cohomology（[@etale_cohomology](https://qiita.com/etale_cohomology)）
