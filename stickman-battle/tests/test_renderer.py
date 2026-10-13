import importlib.util
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("render_battle", ROOT / "scripts" / "render_battle.py")
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)

class RendererTests(unittest.TestCase):
    def test_timeline_has_expected_frame_count(self):
        self.assertEqual(MODULE.FPS * MODULE.DURATION, 1800)

    def test_render_dimensions_and_color_mode(self):
        frame = MODULE.render_frame(0)
        self.assertEqual(frame.size, (960, 540))
        self.assertEqual(frame.mode, "RGB")

    def test_frame_changes_over_time(self):
        self.assertNotEqual(MODULE.render_frame(0).tobytes(), MODULE.render_frame(420).tobytes())

    def test_phase_helpers_are_bounded(self):
        self.assertEqual(MODULE.phase(-1, 0, 1), 0)
        self.assertEqual(MODULE.phase(2, 0, 1), 1)

if __name__ == "__main__":
    unittest.main()
