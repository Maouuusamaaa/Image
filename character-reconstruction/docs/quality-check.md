# Quality check

| Berkas | Dimensi | Format/mode | Status lokal |
|---|---:|---|---|
| `output/final/character-faithful-4096px.png` | 2501 × 4096 | PNG RGB | Lulus buka ulang dan validasi dimensi |
| `output/final/character-faithful-8192px.png` | 5003 × 8192 | PNG RGB | Lulus buka ulang dan validasi dimensi |

Paket lokal memiliki kedua PNG final, referensi sumber, skrip, SVG manual, eksperimen, dokumentasi, dan tes. Hasil PNG adalah upscaling Lanczos, bukan super-resolution generatif. SVG manual masih berbeda dari referensi pada tangan, panel/pola syal, dan beberapa proporsi; karenanya belum dinyatakan pixel-accurate.

Jalankan `python -m unittest discover -s tests -v` untuk pemeriksaan berkas, format, mode, dan dimensi.