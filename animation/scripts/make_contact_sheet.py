"""Create a labelled contact sheet from generated animation frames."""
from pathlib import Path
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
FRAME_DIR = ROOT / "output" / "frames"
OUT = ROOT / "output" / "contact-sheet.png"
FILES = sorted(FRAME_DIR.glob("frame_*.png"))
if not FILES:
    raise SystemExit(f"No rendered frames found in {FRAME_DIR}")
step = max(1, len(FILES)//24)
selected = [(i, FILES[i]) for i in range(0, len(FILES), step)][:24]
cell_w, cell_h, cols = 240, 155, 4
sheet = Image.new("RGB", (cols*cell_w, ((len(selected)+cols-1)//cols)*cell_h), "white")
draw = ImageDraw.Draw(sheet)
for n, (frame_index, path) in enumerate(selected):
    thumb = Image.open(path).convert("RGB")
    thumb.thumbnail((cell_w, 135))
    x, y = (n % cols)*cell_w, (n // cols)*cell_h
    sheet.paste(thumb, (x, y))
    draw.text((x+5, y+137), f"frame {frame_index:04d} / {frame_index/30:.1f}s", fill="black")
OUT.parent.mkdir(parents=True, exist_ok=True)
sheet.save(OUT)
print(f"Contact sheet: {OUT} ({len(selected)} samples)")
