from pypdf import PdfReader
import json, re, sys

path = sys.argv[1]
reader = PdfReader(path)
text = []
for page in reader.pages[:12]:
    try:
        text.append(page.extract_text() or '')
    except Exception as e:
        text.append(f'[ERR:{e}]')
joined = '\n'.join(text)
keywords = [m.group(0) for m in re.finditer(r'(Pauline|Catholic|Acts|Psalm|Gospel|Matthew|Mark|Luke|John|Romans|Corinthians|James|Epistle)', joined, re.I)]
print(json.dumps({'path': path, 'pages': len(reader.pages), 'sample': joined[:5000], 'keyword_hits': keywords[:50]}))
