# Idaho: law history in git

The Constitution of the State of Idaho and titles of the Idaho Statutes as a git repository: one file per section, committed with the Idaho Legislature as its publisher. It follows the shared design of [lexifina/global-law](https://github.com/lexifina/global-law), which places it at `united-states/idaho/`.

**What is in it now**

| Folder | Act | Versions | History |
| --- | --- | ---: | --- |
| `constitution/` | Constitution of the State of Idaho (1890, as amended): Articles I to XXI, 228 sections | 1 | – |
| `title-0005-chapter-*/` | Idaho Statutes, Title 5: Proceedings in civil actions in courts of record: 4 chapters (chapters 2, 3, 4, 5), 97 sections | 1 each | One version: the Legislature's online text, each section from its newest web capture, dated 2026-10-23 |
| `title-0018-chapter-*/` | Idaho Statutes, Title 18: Crimes and punishments: 80 chapters (chapters 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 13, 14, 15, 16, 17, 18, 19, 20, 22, 23, 24, 25, 26, 27, 29, 30, 31, 32, 33, 34, 35, 36, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 54, 55, 56, 57, 58, 59, 60, 61, 63, 64, 65, 66, 67, 68, 69, 70, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89), 857 sections | 1 each | One version: the Legislature's online text, each section from its newest web capture, dated 2026-10-22 |
| `title-0032-chapter-*/` | Idaho Statutes, Title 32: Domestic relations: 15 chapters (chapters 1, 2, 3, 4, 5, 6, 7, 8, 9, 12, 13, 14, 16, 17, 18), 177 sections | 1 each | One version: the Legislature's online text, each section from its newest web capture, dated 2026-10-22 |
| `title-0055-chapter-*/` | Idaho Statutes, Title 55: Property in general: 29 chapters (chapters 1, 2, 3, 4, 5, 6, 8, 9, 10, 11, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32), 379 sections | 1 each | One version: the Legislature's online text, each section from its newest web capture, dated 2026-10-23 |

That is all the law this repository holds today. This is a first build: most of the Idaho Statutes, the session laws and administrative rules are not in it, and it has no amendment history yet.

## Where the text comes from

The Idaho Legislature publishes the Constitution at legislature.idaho.gov/statutesrules/idconst/, one page per article (a list of its sections) and one page per section. Each article page names its sections; each section is its newest capture. The sha256 of the pages is in `data/versions.json`.

The Idaho Statutes are published the same way, one page per chapter (a list of its sections) and one page per section. Chapters that could not be read whole are left out; `REPRODUCE.md` lists them under decisions. Each section keeps its "History:" line, which is part of the Legislature's text.

## Dates

- The pages state no date of their own. The site says the Constitution "is updated to the website July 1 following the legislative session". The latest capture date used dates the single version; sections were captured on different days, which `REPRODUCE.md` lists under decisions. It is the oldest version available, credited to the publisher in the first commit.
- Each chapter of the Idaho Statutes is one version, dated by the newest capture day of its title's section pages (or, if later, the day of the newest law already in the repository, so the history only grows), and credited to the publisher as "oldest version available". The site updates the statutes each 1 July; a section changed after its capture would show its older text here.

## What it does not show

X Sec. 3, Art. XII Sec. 3, Art. XIX Secs. 1 and 2, and Art. XXI Secs. 2 and 3. Twenty-four others come from captures made before 2025 (2021 to November 2024).
- Any amendment history: the Constitution as it stood on earlier dates.
- The other titles of the Idaho Statutes, and the chapters of the titles here that web archives do not hold whole.
- Nothing here is an official publication.

## How it is checked

- Every unit is read back from git on its day and compared with the corpus (`tools/check_repo.py`; results in `REPRODUCE.md`).
