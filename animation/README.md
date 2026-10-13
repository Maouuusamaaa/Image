# Stickman Battle Animation — Rebuilt Source

This directory is the editable source of truth for the current procedural animation iteration. It uses a white stage, black stick figures, fixed-length limbs solved with two-bone inverse kinematics, explicit hand targets, grounded foot targets, and a choreography timeline with scheduled contact events.

## Layout

- `src/rig.py` — rig proportions, reachable target clamping, two-bone IK, pose model.
- `src/render_battle.py` — choreography, contact timeline, renderer, and MP4 encoder.
- `tests/test_renderer.py` — tests for segment lengths, ground placement, contact timing, and render output.
- `output/` — generated MP4 and contact sheet.

## Run

Python 3.10+ and Pillow are required. FFmpeg is required only for MP4 encoding.

```bash
python -m pip install -r requirements.txt
python -m unittest discover -s tests -v
python src/render_battle.py --limit-frames 120 --output output/preview.mp4
```

Generate the full current 12-second, 30 FPS animation:

```bash
python src/render_battle.py
```

Impacts are gated by explicit contact timestamps. Proportions are configured in `Rig`, and attacks are authored in `ATTACKS`.

## Known next-stage work

This is a procedural foundation, not a claim of pixel-perfect reference replication. The attack schedule remains hand-authored and needs detailed frame-by-frame comparison with the supplied reference clips. Feet are placed on the ground in each frame; persistent world-space foot locking during root motion still needs a dedicated stance controller.