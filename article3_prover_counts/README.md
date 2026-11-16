# 第3回：どの定理証明支援系に、研究が集まっているか

連載「Neural Theorem Proving」第3回の記事内で使用した集計コードです。

記事：[【全４回連載（第３回）】どの国が、Neural Theorem Proverの研究開発を牽引しているのか](https://qiita.com/etale_cohomology/items/0c223227c69c34f45305)

## 何を数えるコードか

深層学習を使った定理証明の研究が、**どの定理証明支援系を対象としているか**を数えます。

論文の著者の所属国は、元データに記載がないため集計できません。
そこで、処理系ごとの本数を数え、**その処理系を作った国**と対照させています。

## データ

[zhaoyu-li/DL4TP](https://github.com/zhaoyu-li/DL4TP) の論文一覧を使います。

COLM 2024 の調査論文に付随するリストで、各論文に対象とした処理系のラベルが付いています。

> Zhaoyu Li, Jialiang Sun, Logan Murphy, Qidong Su, Zenan Li, Xian Zhang, Kaiyu Yang, Xujie Si,
> "A Survey on Deep Learning for Theorem Proving," COLM 2024.
> https://arxiv.org/abs/2404.09939

## 使い方

```bash
git clone --depth 1 https://github.com/zhaoyu-li/DL4TP.git
python3 count_systems.py DL4TP/README.md
```

標準ライブラリのみで動きます。依存パッケージはありません。

Python 3.8 以上を想定しています。

## 出力

```
論文数（重複を除く）: 208

--- 対象とした定理証明支援系ごとの論文数 ---
  処理系        論文数   作った国
  Lean             46   アメリカ（Microsoft Research 発、現在は Lean FRO）
  Isabelle         24   イギリス・ドイツ（ケンブリッジ大学、ミュンヘン工科大学）
  Mizar            18   ポーランド（ビャウィストク大学）
  Coq              17   フランス（INRIA）
  HOL Light        12   イギリス（ケンブリッジ大学の系譜）
  Metamath          7   アメリカ

--- 年ごとの推移（上位３つの処理系） ---
    年    合計   Lean  Isabelle   Coq
  2018       4      0         0     0
  2019      13      0         0     2
  2020      29      0         0     4
  2021      29      0         2     1
  2022      26      6         5     2
  2023      50     17         9     6
  2024      37     13         8     2
  2025      10     10         0     0
```

元データの更新により、数字は変わる可能性があります。
記事の数字は、2026年11月時点で取得したものです。

## この集計の限界

- 元リストの最終更新は 2025年5月です。2025年の数字は途中までであり、2026年は含まれていません。
- 1本の論文が複数の処理系を対象にする場合、それぞれに数えています。
- 元リストに収録されていない研究があります。網羅ではありません。
- 著者の所属国は集計していません。元リストに所属の記載がないためです。また、氏名から出身を推定する方法は取っていません。

## ライセンス

リポジトリ直下の LICENSE に従います。
