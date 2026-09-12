"""Generate the PyCarinthia icon set from the source logo.

This is a one-off tool, not part of the site build. Run it only when the
source logo changes; commit the generated files. It needs Pillow, which is
deliberately not a project dependency:

    uv run --with pillow python tools/make_icons.py
"""

from __future__ import annotations

from collections import deque
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "content" / "assets"
SOURCE = ASSETS / "logo.png"

BACKGROUND_TOLERANCE = 24
MARK_PADDING = 0.06
OG_SIZE = (1200, 630)
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

    while queue:
        x, y = queue.popleft()
        if not (0 <= x < width and 0 <= y < height) or visited[y][x]:
            continue
        visited[y][x] = True
        if not matches((x, y)):
            continue
        pixels[x, y] = (0, 0, 0, 0)
        queue.extend(((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)))

    return image


def square_mark(image: Image.Image) -> Image.Image:
    """Crop to the visible mark, then expand to a padded square around it."""
    box = image.getbbox()
    if box is None:
        raise SystemExit("logo has no visible pixels after background removal")

    left, top, right, bottom = box
    side = max(right - left, bottom - top) * (1 + 2 * MARK_PADDING)
    half = side / 2

    mark = Image.new("RGBA", (round(side), round(side)), (0, 0, 0, 0))
    mark.paste(image.crop(box), (round(half - (right - left) / 2), round(half - (bottom - top) / 2)))
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
    transparent.save(SOURCE)
    print(f"wrote {SOURCE.relative_to(ROOT)} ({transparent.width}x{transparent.height}, transparent)")

    mark = square_mark(transparent)
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
