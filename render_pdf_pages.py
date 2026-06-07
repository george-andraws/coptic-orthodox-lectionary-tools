import sys
import fitz
from pathlib import Path
pdf=Path(sys.argv[1])
outdir=Path(sys.argv[2])
outdir.mkdir(parents=True, exist_ok=True)
start=int(sys.argv[3])
end=int(sys.argv[4])
doc=fitz.open(pdf)
for i in range(start,end+1):
    page=doc.load_page(i-1)
    pix=page.get_pixmap(matrix=fitz.Matrix(3,3), alpha=False)
    path=outdir/f'page_{i}.png'
    pix.save(str(path))
    print(path)
