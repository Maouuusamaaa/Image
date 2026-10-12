from pathlib import Path
import unittest
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]

class OutputTests(unittest.TestCase):
    def test_reference_exists(self):
        self.assertTrue((ROOT / "assets" / "reference.jpg").is_file())

    def test_faithful_pngs_integrity_and_dimensions(self):
        expected = {
            "character-faithful-4096px.png": (2501, 4096),
            "character-faithful-8192px.png": (5003, 8192),
        }
        for name, dimensions in expected.items():
            with self.subTest(name=name):
                path = ROOT / "output" / "final" / name
                self.assertTrue(path.is_file(), f"missing {path}")
                with Image.open(path) as image:
                    self.assertEqual(image.format, "PNG")
                    self.assertEqual(image.mode, "RGB")
                    self.assertEqual(image.size, dimensions)
                    image.verify()

if __name__ == "__main__":
    unittest.main()