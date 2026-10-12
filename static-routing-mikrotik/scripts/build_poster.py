#!/usr/bin/env python3
"""Build the A3 static-routing poster into this project's output/ directory."""
from pathlib import Path
import cairosvg

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "source" / "static-routing-mikrotik.svg"
OUT = ROOT / "output"
OUT.mkdir(parents=True, exist_ok=True)

cairosvg.svg2png(
    url=str(SOURCE),
    write_to=str(OUT / "static-routing-mikrotik.png"),
    output_width=1800,
)
cairosvg.svg2pdf(
    url=str(SOURCE),
    write_to=str(OUT / "static-routing-mikrotik.pdf"),
)
print(f"Poster exported to {OUT}")
