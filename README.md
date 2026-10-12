# MikroTik Static Routing Poster

Poster edukasi konfigurasi **static routing dua arah** untuk dua router MikroTik. Format master SVG berbasis vektor; dapat diekspor ke PNG dan PDF.

## Struktur

- `src/static-routing-mikrotik.svg` — master poster vektor A3 portrait.
- `scripts/build_poster.py` — ekspor SVG ke PNG dan PDF.
- `content/static-routing.md` — topologi, alamat IP, dan konfigurasi yang digunakan.
- `dist/` — lokasi hasil ekspor setelah build dijalankan.

## Topologi

- LAN 1: `192.168.1.0/24`, gateway Router 1 `192.168.1.1`
- Link antar-router: `172.16.1.0/30`
- Router 1 transit: `172.16.1.1/30`
- Router 2 transit: `172.16.1.2/30`
- LAN 2: `192.168.2.0/24`, gateway Router 2 `192.168.2.1`

## Build

Gunakan Python 3.10+ dan pasang dependensi:

```bash
python -m pip install cairosvg
python scripts/build_poster.py
```

Output akan dibuat di `dist/static-routing-mikrotik.png` dan `dist/static-routing-mikrotik.pdf`.

## Catatan

Contoh interface memakai `bridge1` untuk LAN dan `ether1` untuk link transit. Sesuaikan nama interface dengan perangkat nyata. Gunakan RouterOS CLI atau WinBox, dan uji konektivitas dari kedua arah. Static route tidak menggantikan konfigurasi IP, gateway klien, atau kebijakan firewall yang sesuai.
