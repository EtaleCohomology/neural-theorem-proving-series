"""
AIが生成した証明と、人間が書いた証明で、have の使い方を比べる。

生成側：DeepSeek-Prover-V2 が miniF2F を解いた証明
  git clone --depth 1 https://github.com/deepseek-ai/DeepSeek-Prover-V2.git
  cd DeepSeek-Prover-V2 && unzip minif2f-solutions.zip -d sol && cd ..

人間側：Mathlib の証明（count_have.py と同じ取得方法）

行数をそろえて比べる点が重要。
生成証明は長いので、全体の平均を比べるだけでは「長いから have が多い」で終わってしまう。
"""
import re
import sys
from pathlib import Path
from count_have import HAVE, split_declarations, strip_comments


def analyze_generated(root):
    """生成された証明。1ファイル1証明。import などのヘッダを落とす。"""
    rows = []
    for f in sorted(Path(root).rglob('*.lean')):
        text = f.read_text(encoding='utf-8')
        i = text.find('theorem ')
        if i < 0:
            continue
        body = strip_comments(text[i:])
        lines = [l for l in body.split('\n') if l.strip()]
        rows.append((len(lines), len(HAVE.findall(body))))
    return rows


def analyze_mathlib(root):
    rows = []
    for f in sorted(Path(root).rglob('*.lean')):
        try:
            text = f.read_text(encoding='utf-8')
        except Exception:
            continue
        for block in split_declarations(text):
            body = strip_comments(block)
            lines = [l for l in body.split('\n') if l.strip()]
            rows.append((len(lines), len(HAVE.findall(body))))
    return rows


def summarize(name, rows):
    n = len(rows)
    with_have = sum(1 for _, h in rows if h > 0)
    total = sum(h for _, h in rows)
    med = sorted(l for l, _ in rows)[n // 2]
    print(f"  {name:26s} {n:7,d}件   中央値 {med:4d}行   "
          f"have を含む {with_have / n * 100:5.1f}%   １件平均 {total / n:5.2f}個")


if __name__ == "__main__":
    gen = analyze_generated(sys.argv[1] if len(sys.argv) > 1 else 'DeepSeek-Prover-V2/sol')
    ml = analyze_mathlib(sys.argv[2] if len(sys.argv) > 2 else 'mathlib4/Mathlib')

    print("=== 全体の比較 ===")
    summarize("生成（DeepSeek-Prover-V2）", gen)
    summarize("人間（Mathlib 全体）", ml)

    print("\n=== 行数をそろえた比較 ===")
    for lo, hi, label in [(1, 10, '1〜10行'), (11, 30, '11〜30行'),
                          (31, 100, '31〜100行'), (101, 10**9, '101行以上')]:
        g = [r for r in gen if lo <= r[0] <= hi]
        m = [r for r in ml if lo <= r[0] <= hi]
        print(f"\n【{label}】")
        if g:
            summarize("生成（DeepSeek-Prover-V2）", g)
        if m:
            summarize("人間（Mathlib）", m)
