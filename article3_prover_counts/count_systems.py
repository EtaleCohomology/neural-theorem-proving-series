"""
定理証明支援系ごとに、深層学習を使った研究が何本あるかを数える。

データ：Deep Learning for Theorem Proving（DL4TP）の論文一覧
  https://github.com/zhaoyu-li/DL4TP
  COLM 2024 の調査論文に付随する、査読を経た論文の整理リスト。
  各論文に、対象とした定理証明支援系のラベルが付いている。

使い方
  git clone --depth 1 https://github.com/zhaoyu-li/DL4TP.git
  python3 count_systems.py DL4TP/README.md
"""
import re
import sys
from collections import Counter, defaultdict

# 本稿で扱う定理証明支援系と、それを作った国
SYSTEMS = {
    'Lean':       'アメリカ（Microsoft Research 発、現在は Lean FRO）',
    'Isabelle':   'イギリス・ドイツ（ケンブリッジ大学、ミュンヘン工科大学）',
    'Coq':        'フランス（INRIA）',
    'Mizar':      'ポーランド（ビャウィストク大学）',
    'HOL Light':  'イギリス（ケンブリッジ大学の系譜）',
    'Metamath':   'アメリカ',
}

ENTRY = re.compile(r'^1\. \*\*(.+?)\*\* `([^`]+)`(.*)$', re.M)


def parse(path):
    """(題名, 会議, 年, ラベルの集合) を返す。重複する論文は題名で一意化する。"""
    text = open(path, encoding='utf-8').read()
    seen = {}
    for title, venue, rest in ENTRY.findall(text):
        m = re.search(r'\[([^\[\]]+)\]\s*$', rest)
        labels = set()
        if m:
            labels = {w.strip() for w in m.group(1).split(',')}
        y = re.search(r'(19|20)\d\d', venue)
        year = int(y.group()) if y else None
        seen[title] = (venue.strip(), year, labels)
    return seen


def main(path):
    papers = parse(path)
    print(f'論文数（重複を除く）: {len(papers)}\n')

    print('--- 対象とした定理証明支援系ごとの論文数 ---')
    print('  処理系        論文数   作った国')
    counts = Counter()
    for _, (_, _, labels) in papers.items():
        for s in SYSTEMS:
            if s in labels:
                counts[s] += 1
    for s, n in counts.most_common():
        print(f'  {s:12s} {n:6d}   {SYSTEMS[s]}')

    print('\n--- 年ごとの推移（上位３つの処理系） ---')
    by_year = defaultdict(Counter)
    for _, (_, year, labels) in papers.items():
        if not year:
            continue
        for s in ('Lean', 'Isabelle', 'Coq'):
            if s in labels:
                by_year[year][s] += 1
        by_year[year]['合計'] += 1
    print('    年    合計   Lean  Isabelle   Coq')
    for y in sorted(by_year):
        if y < 2018:
            continue
        c = by_year[y]
        print(f'  {y}  {c["合計"]:6d} {c["Lean"]:6d} {c["Isabelle"]:9d} {c["Coq"]:5d}')


if __name__ == '__main__':
    main(sys.argv[1] if len(sys.argv) > 1 else 'DL4TP/README.md')
