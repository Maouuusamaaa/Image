#!/usr/bin/env python3
"""Build a reproducible A3 portrait static-routing poster from SVG."""
from pathlib import Path
import cairosvg

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "src" / "static-routing-mikrotik.svg"
OUT = ROOT / "dist"
OUT.mkdir(parents=True, exist_ok=True)

cairosvg.svg2png(url=str(SOURCE), write_to=str(OUT / "static-routing-mikrotik.png"), output_width=1800)
cairosvg.svg2pdf(url=str(SOURCE), write_to=str(OUT / "static-routing-mikrotik.pdf"))
print("Poster exported to dist/")
