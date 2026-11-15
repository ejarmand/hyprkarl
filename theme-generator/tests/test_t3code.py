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

    def test_unknown_artwork_wallpaper_is_an_error(self):
        with self.assertRaisesRegex(GenerationError, "artwork.wallpaper"):
            self.build("gruvbox", "artwork:\n  wallpaper: missing.jpg\n")


if __name__ == "__main__":
    unittest.main()
