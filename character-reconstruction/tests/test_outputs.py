from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]

class ProjectTests(unittest.TestCase):
    def test_project_documentation_and_script_exist(self):
        self.assertTrue((ROOT / "README.md").is_file())
        self.assertTrue((ROOT / "scripts" / "upscale_reference.py").is_file())
        self.assertTrue((ROOT / "docs" / "quality-check.md").is_file())

    def test_reference_if_local_package_includes_it(self):
        reference = ROOT / "assets" / "reference.jpg"
        if not reference.is_file():
            self.skipTest("Binary reference is distributed in the project ZIP, not tracked in this repository.")
        from PIL import Image
        with Image.open(reference) as image:
            self.assertEqual(image.format, "JPEG")
            self.assertEqual(image.size, (938, 1536))

    def test_final_pngs_if_local_package_includes_them(self):
        from PIL import Image
        expected = {
            "character-faithful-4096px.png": (2501, 4096),
            "character-faithful-8192px.png": (5003, 8192),
        }
        output = ROOT / "output" / "final"
        if not all((output / name).is_file() for name in expected):
            self.skipTest("Large PNG outputs are distributed in the project ZIP, not tracked in this repository.")
        for name, dimensions in expected.items():
            with self.subTest(name=name):
                with Image.open(output / name) as image:
                    self.assertEqual(image.format, "PNG")
                    self.assertEqual(image.mode, "RGB")
                    self.assertEqual(image.size, dimensions)
                    image.verify()

if __name__ == "__main__":
    unittest.main()
