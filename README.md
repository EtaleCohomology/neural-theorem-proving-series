# Neural Theorem Proving 連載

Qiita の連載「定理証明を自動で行う Neural Theorem Prover」のコードと資料です。

| 回 | 題名 | コード |
|---|---|---|
| 第１回 | [AIが数学の証明を書けるようになった6年間 ── Neural Theorem Proving の全体像を、正答率30%から99.6%への軌跡とともに読む](https://qiita.com/etale_cohomology/items/4d715c2ce8493cb5225a) | なし |
| 第２回 | [定理証明を自動で行う Neural Theorem Prover は、「タクティク記法」と「宣言的スタイル記法」のどちらで学習し、証明の答案を提出するのか](https://qiita.com/etale_cohomology/items/7f21731d0522935aa1af) | [article2_notation_analysis](article2_notation_analysis) |
| 第３回 | 近日公開 | |
| 第４回 | 近日公開 | |

## 第２回のコード

Lean 4 の証明の中で `have` がどれだけ使われているかを数え、人間が書いた証明とAIが生成した証明を比べるスクリプトです。

Python 3.9 以上だけで動きます。追加のライブラリは不要で、Lean や Mathlib をビルドする必要もありません。

詳しい使い方は [article2_notation_analysis/README.md](article2_notation_analysis/README.md) をご覧ください。

## ライセンス

MIT License

## 作者

Etale Cohomology（[@etale_cohomology](https://qiita.com/etale_cohomology)）
