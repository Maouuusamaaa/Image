#!/usr/bin/env python3
"""High-fidelity non-generative upscale of a supplied reference image."""
from __future__ import annotations
import argparse
from pathlib import Path
from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "assets" / "reference.jpg"
OUTPUT = ROOT / "output" / "final"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--height", type=int, choices=(4096, 8192), default=4096)
    args = parser.parse_args()
    if not SOURCE.is_file():
        raise SystemExit(f"Reference image not found: {SOURCE}")
    OUTPUT.mkdir(parents=True, exist_ok=True)
    with Image.open(SOURCE) as image:
        image = ImageOps.exif_transpose(image).convert("RGB")
        source_width, source_height = image.size
        width = round(args.height * source_width / source_height)
        target = OUTPUT / f"character-faithful-{args.height}px.png"
        image.resize((width, args.height), Image.Resampling.LANCZOS).save(target, format="PNG", optimize=True)
    with Image.open(target) as image:
        image.verify()
    with Image.open(target) as image:
        expected = (round(args.height * source_width / source_height), args.height)
        if image.format != "PNG" or image.mode != "RGB" or image.size != expected:
            raise SystemExit(f"Output validation failed: {image.format}, {image.mode}, {image.size}; expected {expected}")
    print(f"PASS: {target} — {width} × {args.height}, PNG RGB, {target.stat().st_size:,} bytes")
    print("Lanczos interpolation does not create new image detail.")

if __name__ == "__main__":
    main()