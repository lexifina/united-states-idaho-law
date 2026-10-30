"""Bring repo/README.md, repo/LICENSE and repo/jurisdiction.json up to date with the verified Idaho Statutes parts
(corpus.d/title-*.json that have a .PUBLISH sign-off). Idempotent; no network.
    python -X utf8 docs_stat.py
"""
import json, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
R = os.path.join(HERE, 'repo')
NL = '\n'
CD = os.path.join(HERE, 'corpus.d')
parts = sorted(p for p in os.listdir(CD) if p.endswith('.json') and os.path.exists(os.path.join(CD, p[:-5] + '.PUBLISH'))) if os.path.isdir(CD) else []
titles = []
for p in parts:
    acts = json.load(open(os.path.join(CD, p), encoding='utf-8'))['acts']
    t = p[len('title-'):-5]
    name = acts[0]['title'].split('(')[1].split(')')[0]
    nsec = sum(len(a['versions'][0]['units']) for a in acts)
    chs = [a['short'].rsplit('ch. ', 1)[1] for a in acts]
    titles.append((int(re.match(r'\d+', t).group()), t, name, chs, nsec, acts[0]['versions'][0]['from']))
titles.sort()

rd = os.path.join(R, 'README.md')
x = open(rd, encoding='utf-8').read()
x = re.sub(r'\n\| `title-[^\n]*', '', x)
rows = ''.join(f"{NL}| `title-{t.zfill(4)}-chapter-*/` | Idaho Statutes, Title {t}: {name}: {len(chs)} chapters (chapters {', '.join(chs)}), {nsec} sections | 1 each | One version: the Legislature's online text, each section from its newest web capture, dated {day} |"
               for _, t, name, chs, nsec, day in titles)
i = x.index('| `constitution/` |')
j = x.index(NL, i)
x = x[:j] + rows + x[j:]
x = x.replace('The Constitution of the State of Idaho as a git repository: one file per section,',
              'The Constitution of the State of Idaho and titles of the Idaho Statutes as a git repository: one file per section,')
x = re.sub(r'That is all the law this repository holds today\.[^\n]*',
           'That is all the law this repository holds today. This is a first build: most of the Idaho Statutes, the session laws and administrative rules are not in it, and it has no amendment history yet.', x)
src = ('\n\nThe Idaho Statutes are published the same way, one page per chapter (a list of its sections) and one page per '
       'section. A chapter is included only when every section its chapter page lists was read: each section page comes '
       'from its newest **Common Crawl** capture among the 24 newest crawls, or, where Common Crawl had none, its newest '
       '**Internet Archive** capture from 2025 on. Chapters that could not be read whole are left out; `REPRODUCE.md` '
       'lists them under decisions. Each section keeps its "History:" line, which is part of the Legislature\'s text.')
x = x.replace(src, '')
k = x.index('## Dates')
x = x[:k].rstrip(NL) + src + NL + NL + x[k:]
dl = ("- Each chapter of the Idaho Statutes is one version, dated by the newest capture day of its title's section pages "
      "(or, if later, the day of the newest law already in the repository, so the history only grows), and credited to "
      "the publisher as \"oldest version available\". The site updates the statutes each 1 July; a section changed after "
      "its capture would show its older text here.")
x = re.sub(r'\n- Each chapter of the Idaho Statutes is one version[^\n]*', '', x)
k = x.index('## What it does not show')
x = x[:k].rstrip(NL) + NL + dl + NL + NL + x[k:]
x = x.replace('- The Idaho Statutes. Common Crawl holds only part of the statute pages, so they were not taken.',
              '- The other titles of the Idaho Statutes, and the chapters of the titles here that web archives do not hold whole.')
open(rd, 'w', encoding='utf-8', newline=NL).write(x)

lp = os.path.join(R, 'LICENSE')
lt = open(lp, encoding='utf-8').read()
para = ('The Idaho Statutes titles are the text published by the Idaho Legislature at https://legislature.idaho.gov/statutesrules/idstat/ ,'
        + NL + 'read from Common Crawl and Internet Archive captures of its pages (2025 and 2026). Statute text is not copyrightable'
        + NL + 'in the United States (Georgia v. Public.Resource.Org, above); no annotations are used.')
if titles and para not in lt:
    k = lt.index('The arrangement of this repository')
    lt = lt[:k] + para + NL + NL + lt[k:]
    open(lp, 'w', encoding='utf-8', newline=NL).write(lt)

jp = os.path.join(R, 'jurisdiction.json')
j = json.load(open(jp, encoding='utf-8'))
base = j['build'].split('; plus Idaho Statutes')[0]
if titles:
    base += '; plus Idaho Statutes ' + ', '.join(f'Title {t} ({len(chs)} chapters)' for _, t, _, chs, _, _ in titles) + ' (one version each, from web captures)'
j['build'] = base
open(jp, 'w', encoding='utf-8', newline=NL).write(json.dumps(j, ensure_ascii=False, indent=2) + NL)
print(len(titles), 'titles in docs')
