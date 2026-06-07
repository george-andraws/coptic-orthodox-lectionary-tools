import csv
import re
from collections import OrderedDict
from pathlib import Path
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

INDEX_URL = 'https://st-takla.org/Full-Free-Coptic-Books/Coptic-Synaxarium-or-Synaxarion_English/Eng-Synexarium-or-Synexarion-index.html'
ROOT = Path(__file__).resolve().parent
OUT = ROOT / 'out_synaxarium'
OUT.mkdir(parents=True, exist_ok=True)


def clean(s: str) -> str:
    return ' '.join((s or '').split())


html = requests.get(INDEX_URL, timeout=40).text
soup = BeautifulSoup(html, 'html.parser')

month_links = []
for a in soup.find_all('a', href=True):
    href = a['href']
    txt = clean(a.get_text(' ', strip=True))
    if re.fullmatch(r'\d+-.*', txt) and href.endswith('-Coptic-Month.html'):
        month_links.append((txt, urljoin(INDEX_URL, href)))

seen = set()
months = []
for txt, href in month_links:
    if href not in seen:
        months.append((txt, href))
        seen.add(href)

rows = []
for month_title, month_url in months:
    mhtml = requests.get(month_url, timeout=40).text
    msoup = BeautifulSoup(mhtml, 'html.parser')
    day_urls = []
    for a in msoup.find_all('a', href=True):
        href = urljoin(month_url, a['href'])
        if href.endswith('.html') and re.search(r'/Coptic-Calendar_\d{2}-[^/]+\.html$', href):
            day_urls.append(href)
    day_urls = list(dict.fromkeys(day_urls))
    for day_url in day_urls:
        try:
            dhtml = requests.get(day_url, timeout=40).text
            dsoup = BeautifulSoup(dhtml, 'html.parser')
            h1 = dsoup.find('h1')
            day_title = clean(h1.get_text(' ', strip=True)) if h1 else ''
            summary = []
            body = dsoup.find(id='bodytext') or dsoup.body
            if body:
                for tag in body.find_all(['p', 'li', 'h2', 'h3'], recursive=True):
                    txt = clean(tag.get_text(' ', strip=True))
                    if not txt:
                        continue
                    if txt.startswith('Coptic Synaxarium'):
                        continue
                    if txt.startswith('Days of the month of'):
                        continue
                    if txt.startswith('Site Search') or txt.startswith('Gallery Search'):
                        continue
                    if txt == 'Search':
                        continue
                    summary.append(txt)
                    if len(summary) >= 4:
                        break
            rows.append({
                'month_title': month_title,
                'month_url': month_url,
                'day_url': day_url,
                'day_title': day_title,
                'summary_lines': ' | '.join(summary),
            })
        except Exception as e:
            rows.append({
                'month_title': month_title,
                'month_url': month_url,
                'day_url': day_url,
                'day_title': '',
                'summary_lines': f'ERROR: {e}',
            })

csv_path = OUT / 'synaxarium_day_index.csv'
with csv_path.open('w', newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=['month_title', 'month_url', 'day_url', 'day_title', 'summary_lines'])
    w.writeheader(); w.writerows(rows)

month_groups = OrderedDict()
for r in rows:
    month_groups.setdefault((r['month_title'], r['month_url']), []).append(r)

md = [
    '# Coptic Synaxarium index',
    '',
    'This index maps the public St-Takla daily Synaxarium pages by Coptic month and day, with a short event summary for each page.',
    '',
    '## Why it exists',
    '',
    '- convert Gregorian date to Coptic date',
    '- find the Synaxarium day page',
    '- see the saints or events commemorated on that day',
    '- link the day back to the Coptic lectionary readings for the same date',
    '',
    '## Caution',
    '',
    'This is an index and source map, not a substitute for the full Synaxarium text. When exact wording matters, open the linked page.',
    '',
]
for (month_title, month_url), rs in month_groups.items():
    md.append(f'## {month_title}')
    md.append(f'- Month page: {month_url}')
    for r in rs:
        title = r['day_title'] or r['day_url'].rsplit('/',1)[-1]
        md.append(f'- [{title}]({r["day_url"]})')
        if r['summary_lines']:
            md.append(f'  - {r["summary_lines"][:260]}')
    md.append('')

md_path = OUT / 'synaxarium_index.md'
md_path.write_text('\n'.join(md), encoding='utf-8')
print({'rows': len(rows), 'months': len(month_groups), 'csv': str(csv_path), 'md': str(md_path)})