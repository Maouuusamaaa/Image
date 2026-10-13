# Stickman Battle Animation

A deterministic, code-drawn cinematic stickman scene built with Python/Pillow and encoded with FFmpeg.

## Target
- 30 seconds, 60 FPS, 1,800 frames
- 960×540 (16:9)
- Two consistent procedural stickman rigs, cyan and amber identifiers
- Non-graphic, stylized choreography with dodges, counters, acrobatic beats, impact arcs, and a final standoff

## Layout
```text
stickman-battle/
├── source/       # character rig notes
├── scripts/      # deterministic renderer and MP4 encoder
├── animated/     # numbered PNG frames, grouped by scene
├── output/       # rendered MP4 files
├── docs/         # production notes
├── tests/        # renderer checks
└── requirements.txt
```

## Run
Install FFmpeg separately, then from this directory:

```bash
python -m pip install -r requirements.txt
python scripts/render_battle.py
```

The script writes PNG frames to `animated/scene-01/` and the H.264 video to `output/stickman-battle-scene-01.mp4`. To run a short smoke test:

```bash
python scripts/render_battle.py --limit-frames 120 --output output/preview.mp4
python -m unittest discover -s tests -v
```

Generated frames and videos are build artifacts and are packaged separately rather than committing thousands of binary files to Git history.
