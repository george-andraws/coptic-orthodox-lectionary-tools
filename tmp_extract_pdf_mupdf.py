import sys
import fitz
from pathlib import Path
pdf = Path(sys.argv[1])
out = []
doc = fitz.open(pdf)
for i, page in enumerate(doc):
    try:
        txt = page.get_text("text") or ""
    except Exception as e:
        txt = f"[ERR page {i+1}: {e}]"
    out.append(f"\n===== PAGE {i+1} =====\n{txt}")
print("\n".join(out))
