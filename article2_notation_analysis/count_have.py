"""
Mathlib の証明の中で、`have` がどれだけ使われているかを数える。

使い方
  git clone --depth 1 --filter=blob:none --sparse https://github.com/leanprover-community/mathlib4.git
  cd mathlib4 && git sparse-checkout set Mathlib && cd ..
  python3 count_have.py mathlib4/Mathlib

注意：Lean 4 の構文を正確に解析しているわけではない。
行頭の字句を見る単純な方法で、おおよその傾向をつかむためのもの。
"""
import re
import sys
from collections import Counter
from pathlib import Path

# theorem / lemma の宣言を拾う
DECL = re.compile(
    r'^\s*(?:@\[[^\]]*\]\s*)?'
    r'(?:private\s+|protected\s+|nonrec\s+|noncomputable\s+)*'
    r'(theorem|lemma)\s')

# have の出現。行頭、空白の後、· の後、<;> の後を数える
HAVE = re.compile(r'(?:^|\s|·\s*|<;>\s*)have\s')

BUCKETS = [(1, 1, '1行'), (2, 3, '2〜3行'), (4, 10, '4〜10行'),
           (11, 30, '11〜30行'), (31, 100, '31〜100行'), (101, 10**9, '101行以上')]


def split_declarations(text):
    """ファイルを宣言の単位に粗く分割する。字下げのない行を区切りとみなす。"""
    lines = text.split('\n')
    blocks, cur, in_decl = [], [], False
    for ln in lines:
        if DECL.match(ln):
            if in_decl and cur:
                blocks.append('\n'.join(cur))
            cur, in_decl = [ln], True
        elif in_decl:
            if ln.strip() and not ln[0].isspace() and not ln.lstrip().startswith(('|', '·')):
                blocks.append('\n'.join(cur))
                cur, in_decl = [], False
            else:
                cur.append(ln)
    if in_decl and cur:
        blocks.append('\n'.join(cur))
    return blocks


def strip_comments(block):
    body = re.sub(r'--.*', '', block)
    return re.sub(r'/-.*?-/', '', body, flags=re.S)


def bucket(n):
    for lo, hi, name in BUCKETS:
        if lo <= n <= hi:
            return name
    return BUCKETS[-1][2]


def main(root):
    rows = []                      # (行数, have の個数)
    for f in sorted(Path(root).rglob('*.lean')):
        try:
            text = f.read_text(encoding='utf-8')
        except Exception:
            continue
        for block in split_declarations(text):
            body = strip_comments(block)
            lines = [l for l in body.split('\n') if l.strip()]
            rows.append((len(lines), len(HAVE.findall(body))))

    n = len(rows)
    with_have = sum(1 for _, h in rows if h > 0)
    total = sum(h for _, h in rows)
    print(f"定理・補題の数   : {n:,}")
    print(f"have を含むもの  : {with_have:,} 件 ({with_have / n * 100:.1f}%)")
    print(f"１件あたり平均   : {total / n:.2f} 個\n")

    print("--- 証明の長さ別 ---")
    print("  証明の長さ      定理の数   have を含む割合   １件あたりの have")
    for _, _, name in BUCKETS:
        sub = [r for r in rows if bucket(r[0]) == name]
        if not sub:
            continue
        w = sum(1 for _, h in sub if h > 0)
        t = sum(h for _, h in sub)
        print(f"  {name:12s} {len(sub):10,d}   {w / len(sub) * 100:12.1f}%   {t / len(sub):14.2f}")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else 'mathlib4/Mathlib')
