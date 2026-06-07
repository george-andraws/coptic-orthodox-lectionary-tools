from pypdf import PdfReader
import sys
from pathlib import Path
path = Path(sys.argv[1])
reader = PdfReader(str(path))
parts = []
for page in reader.pages:
    try:
        parts.append(page.extract_text() or '')
    except Exception as e:
        parts.append(f'[ERR:{e}]')
print('\n'.join(parts))
