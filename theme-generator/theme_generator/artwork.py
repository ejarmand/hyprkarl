import base64
import io
from pathlib import Path

from PIL import Image, ImageFilter


# T3 Code takes at most 20,000 characters of custom CSS, and base64 grows the
# image by a third, so the encoded crop stays under about 10 KB. Painted
# brushwork compresses poorly; a slight blur and a falling width keep detail
# where the budget allows.
MAX_BYTES = 10_500
WIDTHS = (360, 300, 240)
QUALITIES = (40, 35, 30, 25, 20)
BLUR_RADIUS = 0.7


def artwork_data_uri(path: Path, crop: list[float]) -> str:
    """Crop a wallpaper to `crop` (left, top, width, height as fractions) and
    return it as a small WebP data URI."""
    left, top, width, height = crop
    with Image.open(path) as source:
        image = source.convert("RGB")
    box = (
        round(left * image.width),
        round(top * image.height),
        round((left + width) * image.width),
        round((top + height) * image.height),
    )
    image = image.crop(box).filter(ImageFilter.GaussianBlur(BLUR_RADIUS))

    for target_width in WIDTHS:
        resized = image.resize(
            (target_width, round(target_width * image.height / image.width)),
            Image.Resampling.LANCZOS,
        )
        for quality in QUALITIES:
            buffer = io.BytesIO()
            resized.save(buffer, format="WEBP", quality=quality, method=6)
            if buffer.tell() <= MAX_BYTES:
                encoded = base64.b64encode(buffer.getvalue()).decode()
                return f"data:image/webp;base64,{encoded}"
    raise ValueError(f"Artwork crop of {path.name} does not fit in {MAX_BYTES} bytes")
