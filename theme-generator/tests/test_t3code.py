import json
import shutil
import tempfile
import unittest
from pathlib import Path

from theme_generator.render import GenerationError, build_theme


# T3 Code ignores a theme file over 32 KiB or with more than 20,000 characters
# of custom CSS.
MAX_FILE_BYTES = 32768
MAX_CSS_CHARACTERS = 20000


class T3CodeThemeTests(unittest.TestCase):
    def build(self, theme: str, overlay_text: str | None = None) -> Path:
        directory = Path(tempfile.mkdtemp(prefix="t3code-theme-"))
        self.addCleanup(shutil.rmtree, directory, ignore_errors=True)
        overlay = None
        if overlay_text is not None:
            overlay = directory / "overlay"
            overlay.mkdir()
            (overlay / "theme.yaml").write_text(overlay_text)
        output = directory / "output"
        build_theme(theme, output, overlay_source=overlay)
        return output / "t3code.json"

    def test_artwork_embeds_a_painting_within_t3_limits(self):
        path = self.build("van-gogh-crabs")
        theme = json.loads(path.read_text())

        self.assertEqual(theme["canvas"], "#10201c")
        self.assertIn("data:image/webp;base64,", theme["css"])
        self.assertLessEqual(len(theme["css"]), MAX_CSS_CHARACTERS)
        self.assertLessEqual(path.stat().st_size, MAX_FILE_BYTES)

    def test_theme_without_artwork_has_only_colors(self):
        theme = json.loads(self.build("gruvbox").read_text())

        self.assertNotIn("css", theme)
        self.assertEqual(theme["appearance"], "dark")

    def test_personal_css_follows_the_painting(self):
        theme = json.loads(
            self.build("van-gogh-crabs", 't3code:\n  css: "body{opacity:1}"\n').read_text()
        )

        self.assertTrue(theme["css"].endswith("\nbody{opacity:1}"))

    def test_artwork_survives_removing_its_wallpaper_from_the_rotation(self):
        directory = Path(tempfile.mkdtemp(prefix="t3code-theme-"))
        self.addCleanup(shutil.rmtree, directory, ignore_errors=True)
        overlay = directory / "overlay"
        overlay.mkdir()
        (overlay / ".wallpapers-disabled").write_text("01-crabs-crop.jpg\n")
        output = directory / "output"
        build_theme("van-gogh-crabs", output, overlay_source=overlay)

        self.assertFalse((output / "wallpapers" / "01-crabs-crop.jpg").exists())
        self.assertIn("data:image/webp", json.loads((output / "t3code.json").read_text())["css"])

    def test_any_t3_sidebar_color_works_with_artwork(self):
        theme = json.loads(
            self.build(
                "van-gogh-crabs", 't3code:\n  colors:\n    sidebar: "oklch(0.3 0.04 160)"\n'
            ).read_text()
        )

        self.assertIn("color-mix(in srgb,oklch(0.3 0.04 160) 30%,transparent)", theme["css"])

    def test_css_over_t3_limit_is_an_error(self):
        with self.assertRaisesRegex(GenerationError, "T3 Code's limits"):
            self.build("van-gogh-crabs", f't3code:\n  css: "/*{"x" * 10000}*/"\n')

    def test_unknown_artwork_wallpaper_is_an_error(self):
        with self.assertRaisesRegex(GenerationError, "artwork.wallpaper"):
            self.build("gruvbox", "artwork:\n  wallpaper: missing.jpg\n")


if __name__ == "__main__":
    unittest.main()
