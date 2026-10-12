# Production notes — Scene 01

- Style: cinematic, stylized, non-graphic hand-to-hand choreography.
- Duration: 30 seconds.
- Frame rate: 60 FPS (1,800 frames).
- Logical render size: 960×540 (16:9); output is H.264 MP4, yuv420p.
- Character consistency: shared fixed-proportion procedural rig; only pose joints, location, and small camera effects vary.
- Motion design: eased approach, feints, dodges, acrobatic exchanges, stylized impact arcs, recovery, and final standoff.
- All visual elements are drawn in code using Pillow. MP4 encoding uses FFmpeg.

## Regenerate

```bash
python -m pip install -r requirements.txt
python scripts/render_battle.py
``

For a quick preview:

```bash
python scripts/render_battle.py --limit-frames 120 --output output/preview.mp4
``

PNG frames are written to `animated/scene-01/`; the MP4 is written to `output/`.
