"""Generate the PyCarinthia raster icons from the source logo.

This is a one-off tool, not part of the site build. `logo.svg` is the source
of truth — replace that file when the logo changes. The site shows the SVG
directly; every PNG/ICO this script writes is a derived output, generated
fresh from the SVG each run. Commit the generated files alongside the
source. This needs Pillow and resvg, which are deliberately not project
dependencies:

    uv run --with pillow --with resvg-py python tools/make_icons.py
"""

from __future__ import annotations

import io
from pathlib import Path

import resvg_py
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "content" / "assets"
SOURCE = ASSETS / "logo.svg"

# Edge length the SVG is rasterised at before any resizing. Large enough that
# every derived icon is a downscale.
RENDER_SIZE = 2048

# Extra margin added around the cropped mark, as a fraction of its longest
# side, before squaring it off. Raise for more breathing room around the
# mark in the square icons; lower to make the mark fill more of the frame.
MARK_PADDING = 0.06

OG_SIZE = (1200, 630)

# Width of the mark relative to the og-image canvas width. Raise to make the
# logo more prominent in social previews; lower to leave more white margin.
OG_LOGO_WIDTH_RATIO = 0.25


def render(path: Path) -> Image.Image:
    """Rasterise the SVG onto a transparent canvas, keeping its aspect ratio."""
    png = resvg_py.svg_to_bytes(svg_path=str(path), width=RENDER_SIZE)
    return Image.open(io.BytesIO(bytes(png))).convert("RGBA")


def square_mark(image: Image.Image) -> Image.Image:
    """Crop to the visible mark, then expand to a padded square around it."""
    box = image.getbbox()
    if box is None:
        raise ValueError("logo has no visible pixels; check that logo.svg renders")

    left, top, right, bottom = box
    side = round(max(right - left, bottom - top) * (1 + 2 * MARK_PADDING))
    half = side // 2

    mark = Image.new("RGBA", (side, side), (0, 0, 0, 0))
    mark.paste(image.crop(box), (half - (right - left) // 2, half - (bottom - top) // 2))
    return mark


def on_white(image: Image.Image, size: tuple[int, int], logo_width: int) -> Image.Image:
    """Composite the logo onto an opaque white canvas of the given size."""
    canvas = Image.new("RGBA", size, (255, 255, 255, 255))
    scale = logo_width / image.width
    scaled = image.resize((logo_width, round(image.height * scale)), Image.LANCZOS)
    canvas.alpha_composite(
        scaled,
        ((size[0] - scaled.width) // 2, (size[1] - scaled.height) // 2),
    )
    return canvas.convert("RGB")


def main() -> None:
    rendered = render(SOURCE)

    # Fail before writing anything if the SVG gained an opaque background,
    # which would show up as a white square on the dark theme.
    if rendered.getpixel((0, 0))[3] != 0:
        raise ValueError("logo.svg has an opaque background; the mark must sit on transparency")

    mark = square_mark(rendered)

    for size in (192, 512):
        mark.resize((size, size), Image.LANCZOS).save(ASSETS / f"icon-{size}.png")
        print(f"wrote content/assets/icon-{size}.png ({size}x{size})")

    # iOS discards alpha and composites onto black, so bake in a white background.
    on_white(mark, (180, 180), 180).save(ASSETS / "apple-touch-icon.png")
    print("wrote content/assets/apple-touch-icon.png (180x180, opaque)")

    mark.save(ASSETS / "favicon.ico", sizes=[(16, 16), (32, 32), (48, 48)])
    print("wrote content/assets/favicon.ico (16, 32, 48)")

    on_white(mark, OG_SIZE, round(OG_SIZE[0] * OG_LOGO_WIDTH_RATIO)).save(ASSETS / "og-image.png")
    print(f"wrote content/assets/og-image.png ({OG_SIZE[0]}x{OG_SIZE[1]})")


if __name__ == "__main__":
    main()
