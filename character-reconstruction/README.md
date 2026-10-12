# Character Reconstruction

Proyek ini berfokus pada mempertahankan kemiripan visual terhadap gambar referensi dan menyimpan seluruh berkas per karya di folder khusus.

## Isi proyek

- `assets/reference.jpg` — gambar sumber (disertakan dalam paket proyek lokal; jangan menganggapnya ada di checkout GitHub jika tidak diunggah).
- `scripts/upscale_reference.py` — upscale PNG 4K/8K dengan Lanczos; tidak mengklaim membuat detail baru.
- `source/character.svg` — master SVG manual yang dapat diedit, tetapi masih merupakan interpretasi dan belum pixel-accurate.
- `output/final/` — PNG fidelity tinggi hasil lokal.
- `output/experiments/` — render lama dan eksperimen, dipisahkan dari hasil final.
- `docs/` dan `tests/` — keputusan teknis serta pemeriksaan otomatis.

## Menjalankan

```bash
python -m pip install pillow cairosvg
python scripts/upscale_reference.py --height 4096
python scripts/upscale_reference.py --height 8192
python -m unittest discover -s tests -v
```

Sediakan `assets/reference.jpg` dari sumber yang sah sebelum menjalankan skrip. Output memakai rasio sumber dan disimpan ke `output/final/`. Lanczos meningkatkan dimensi, bukan informasi detail asli.

## Status

PNG 4K (2501 × 4096) dan 8K (5003 × 8192) sudah lulus pemeriksaan integritas pada paket lokal. SVG manual belum setara secara visual dengan referensi; keterbatasan dijelaskan dalam `docs/quality-check.md`.