# Image Projects

Repositori untuk menyimpan proyek gambar dan animasi secara rapi. **Setiap karya memiliki folder proyek sendiri**; sumber, skrip, hasil akhir, dan dokumentasi tidak dicampur dengan proyek lain.

## Struktur standar

```text
nama-proyek/
├── README.md
├── assets/
├── source/
├── scripts/
├── animated/
├── output/
├── tests/
└── docs/
```

## Proyek

- [Static Routing MikroTik](static-routing-mikrotik/) — poster edukasi A3 tentang static routing dua router.
- [Character Reconstruction](character-reconstruction/) — pipeline upscale gambar referensi dengan validasi PNG 4K/8K; master SVG manual memiliki batasan yang didokumentasikan.
- [Stickman Battle Animation](stickman-battle/) — animasi stickman sinematik berbasis kode, frame PNG berurutan, dan render MP4 30 detik pada 60 FPS.

Setiap proyek harus diperiksa hasilnya sebelum ditandai selesai. File sementara dan frame hasil render disimpan di dalam folder proyek terkait, bukan di root repositori.
