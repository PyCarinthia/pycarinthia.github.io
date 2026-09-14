"""Generate the PyCarinthia icon set from the source logo.

This is a one-off tool, not part of the site build. `logo-source.png` is the
pristine, opaque original — replace that file when the logo changes. Every
other file this script writes, including `content/assets/logo.png`, is a
derived output: it is generated fresh from the source each run and must
never be read back as input. Commit the generated files alongside the
source. This needs Pillow, which is deliberately not a project dependency:

    uv run --with pillow python tools/make_icons.py
"""

from __future__ import annotations

from collections import deque
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "content" / "assets"
SOURCE = ASSETS / "logo-source.png"

# How far a pixel's RGB may drift from the detected background seed and still
# be flood-filled away. Raise this if a background halo survives around the
# mark; lower it if the fill eats into the snow caps or the two white dots.
BACKGROUND_TOLERANCE = 24

# Extra margin added around the cropped mark, as a fraction of its longest
# side, before squaring it off. Raise for more breathing room around the
# mark in the square icons; lower to make the mark fill more of the frame.
MARK_PADDING = 0.06

OG_SIZE = (1200, 630)

# Width of the logo relative to the og-image canvas width. Raise to make the
# logo more prominent in social previews; lower to leave more white margin.
OG_LOGO_WIDTH_RATIO = 0.6


def strip_background(image: Image.Image) -> Image.Image:
    """Make the outer background transparent via a flood fill from the border.

    Only pixels connected to the image edge are cleared, so white areas inside
    the mark (snow, river highlights, the two dots) keep their colour.
    """
    image = image.convert("RGBA")
    width, height = image.size
    pixels = image.load()
    seed = pixels[0, 0][:3]
    print(f"background seed colour: {seed}")

    if any(component < 255 - BACKGROUND_TOLERANCE for component in seed):
        raise ValueError(
            f"background seed {seed} at pixel (0, 0) is not close to white; "
            "check that the source's corners are plain background, not artwork, "
            "and not already transparent"
        )

    def matches(xy: tuple[int, int]) -> bool:
        red, green, blue, alpha = pixels[xy]
        if alpha == 0:
            return False
        return all(abs(a - b) <= BACKGROUND_TOLERANCE for a, b in zip((red, green, blue), seed))

    visited = [[False] * width for _ in range(height)]
    queue: deque[tuple[int, int]] = deque()

    for x in range(width):
        for y in (0, height - 1):
            queue.append((x, y))
    for y in range(height):
        for x in (0, width - 1):
            queue.append((x, y))

    cleared = 0
    while queue:
        x, y = queue.popleft()
        if not (0 <= x < width and 0 <= y < height) or visited[y][x]:
            continue
        visited[y][x] = True
        if not matches((x, y)):
            continue
        pixels[x, y] = (0, 0, 0, 0)
        cleared += 1
        queue.extend(((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)))

    if cleared == 0:
        raise ValueError(
            "background flood fill cleared no pixels; BACKGROUND_TOLERANCE "
            f"({BACKGROUND_TOLERANCE}) may be too low for this source, or the "
            "border is not a solid background colour"
        )
    print(f"background flood fill cleared {cleared} pixels")

    return image


def square_mark(image: Image.Image) -> Image.Image:
    """Crop to the visible mark, then expand to a padded square around it."""
    box = image.getbbox()
    if box is None:
        raise ValueError(
            "logo has no visible pixels after background removal; check "
            "BACKGROUND_TOLERANCE and the source image"
        )

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
    source = Image.open(SOURCE)
    transparent = strip_background(source)

    # All checks above have passed; only now do we start writing files.
    mark = square_mark(transparent)

    transparent.save(ASSETS / "logo.png")
    print(f"wrote content/assets/logo.png ({transparent.width}x{transparent.height}, transparent)")

    mark.save(ASSETS / "logo-mark.png")
    print(f"wrote content/assets/logo-mark.png ({mark.width}x{mark.height})")

    for size in (192, 512):
        mark.resize((size, size), Image.LANCZOS).save(ASSETS / f"icon-{size}.png")
        print(f"wrote content/assets/icon-{size}.png ({size}x{size})")

    # iOS discards alpha and composites onto black, so bake in a white background.
    on_white(mark, (180, 180), 180).save(ASSETS / "apple-touch-icon.png")
    print("wrote content/assets/apple-touch-icon.png (180x180, opaque)")

    mark.save(ASSETS / "favicon.ico", sizes=[(16, 16), (32, 32), (48, 48)])
    print("wrote content/assets/favicon.ico (16, 32, 48)")

    on_white(transparent, OG_SIZE, round(OG_SIZE[0] * OG_LOGO_WIDTH_RATIO)).save(ASSETS / "og-image.png")
    print(f"wrote content/assets/og-image.png ({OG_SIZE[0]}x{OG_SIZE[1]})")


if __name__ == "__main__":
    main()
