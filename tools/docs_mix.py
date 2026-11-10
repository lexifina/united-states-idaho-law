"""Brings repo/README.md and repo/jurisdiction.json up to date with every signed-off Idaho Statutes part
(corpus.d/title-*.json, including title-<t>-more.json parts that add chapters to a title). One row per title.
Starts from the published README. No network.
    python -X utf8 docs_mix.py
"""
import json, os, re
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
R = os.path.join(HERE, 'repo')
NL = '\n'
CD = os.path.join(HERE, 'corpus.d')
parts = sorted(p for p in os.listdir(CD) if p.endswith('.json') and os.path.exists(os.path.join(CD, p[:-5] + '.PUBLISH')))
by = defaultdict(lambda: {'name': '', 'chs': [], 'nsec': 0, 'days': set()})
for p in parts:
    for a in json.load(open(os.path.join(CD, p), encoding='utf-8'))['acts']:
        t = re.match(r'Idaho Code tit\. (\w+), ch\. (\w+)', a['short'])
        r = by[t.group(1)]
        r['name'] = a['title'].split('(', 1)[1].split('), Chapter', 1)[0]
        r['chs'].append(t.group(2))
        r['nsec'] += len(a['versions'][0]['units'])
        r['days'].add(a['versions'][0]['from'])


def k(x):
    return [int(y) if y.isdigit() else y for y in re.split(r'(\d+)', x)]


rows = ''
for t in sorted(by, key=k):
    r = by[t]
    chs = sorted(set(r['chs']), key=k)
    d = sorted(r['days'])
    when = d[0] if len(d) == 1 else f'{d[0]} to {d[-1]}'
    rows += (f"{NL}| `title-{t.zfill(4)}-chapter-*/` | Idaho Statutes, Title {t}: {r['name']}: {len(chs)} chapters (chapters {', '.join(chs)}), "
             f"{r['nsec']} sections | 1 each | One version: the Legislature's online text, each section from its newest web capture, dated {when} |")
x = open(os.path.join(R, 'README.md'), encoding='utf-8').read()
x = re.sub(r'\n\| `title-[^\n]*', '', x)
i = x.index('| `constitution/` |')
j = x.index(NL, i)
x = x[:j] + rows + x[j:]
add = ('- Chapters added from 2026-11-10 on are each dated by the newest capture day among their own chapter page and '
       'section pages, never moved later; the chapters published before keep their dates.')
x = re.sub(r'\n- Chapters added from 2026-11-10[^\n]*', '', x)
kk = x.index('## What it does not show')
x = x[:kk].rstrip(NL) + NL + add + NL + NL + x[kk:]
open(os.path.join(R, 'README.md'), 'w', encoding='utf-8', newline=NL).write(x)
jp = os.path.join(R, 'jurisdiction.json')
j = json.load(open(jp, encoding='utf-8'))
nch = sum(len(set(r['chs'])) for r in by.values())
j['build'] = f'built: Constitution and {nch} chapters of the Idaho Statutes in {len(by)} titles, one version each from web captures'
open(jp, 'w', encoding='utf-8', newline=NL).write(json.dumps(j, ensure_ascii=False, indent=2) + NL)
print(len(by), 'titles', nch, 'chapters')
