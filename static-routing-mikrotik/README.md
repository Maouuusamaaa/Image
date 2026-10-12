# Poster Static Routing MikroTik

Poster edukasi konfigurasi **static routing dua arah** pada dua router MikroTik, dengan format master SVG A3 portrait.

## Folder proyek

- `source/static-routing-mikrotik.svg` — master poster vektor.
- `scripts/build_poster.py` — mengekspor master SVG menjadi PNG dan PDF.
- `output/` — hasil ekspor lokal: PNG dan PDF.
- `docs/static-routing.md` — skema IP, contoh konfigurasi, dan langkah verifikasi.

## Build

Persyaratan: Python 3.10+ dan CairoSVG.

```bash
python -m pip install cairosvg
python scripts/build_poster.py
```

Hasil dibuat di `output/static-routing-mikrotik.png` dan `output/static-routing-mikrotik.pdf`.

## Topologi

- LAN 1: `192.168.1.0/24`, gateway R1 `192.168.1.1`
- Link antar-router: `172.16.1.0/30`
- Transit R1: `172.16.1.1/30`
- Transit R2: `172.16.1.2/30`
- LAN 2: `192.168.2.0/24`, gateway R2 `192.168.2.1`

Nama interface pada contoh adalah `bridge1` untuk LAN dan `ether1` untuk link transit. Sesuaikan dengan konfigurasi perangkat sebenarnya.
