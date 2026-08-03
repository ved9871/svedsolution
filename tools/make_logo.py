# -*- coding: utf-8 -*-
"""
Renders the SVED Solution logo and favicon set as PNG.

Drawn directly with Pillow rather than converted from the SVG: SVG rasterisers
need native Cairo on Windows, and drawing here gives exact control over the
gradient, the mark geometry and the hinting at 16px.

    python tools/make_logo.py
"""
import os
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONTS = os.path.join(ROOT, ".fonts")
ASSETS = os.path.join(ROOT, "assets")
BRAND = os.path.join(ROOT, "brand")

GREEN = (0, 255, 178)
BLUE = (0, 165, 255)
INK = (7, 12, 18)
WHITE = (255, 255, 255)
NAVY = (11, 18, 25)
MUTED = (132, 150, 169)

SS = 4  # supersample factor; everything is drawn large then downsampled


def font(name, size):
    path = os.path.join(FONTS, name)
    if os.path.exists(path):
        return ImageFont.truetype(path, size)
    for fallback in ("segoeuib.ttf", "arialbd.ttf", "seguisb.ttf", "arial.ttf"):
        p = os.path.join(os.environ.get("WINDIR", "C:/Windows"), "Fonts", fallback)
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()


def gradient(size, a, b, steps=192):
    """
    Diagonal two-stop gradient matching the SVG's 0,0 -> 1,1 direction.

    Built at a small fixed resolution and scaled up: a per-pixel Python loop is
    O(n^2) and takes minutes at the supersampled sizes used here, while a smooth
    two-stop ramp upscales without any visible banding.
    """
    small = Image.new("RGB", (steps, steps))
    px = small.load()
    denom = max(steps - 1, 1)
    for y in range(steps):
        for x in range(steps):
            t = (x + y) / (2 * denom)
            px[x, y] = (
                int(a[0] + (b[0] - a[0]) * t),
                int(a[1] + (b[1] - a[1]) * t),
                int(a[2] + (b[2] - a[2]) * t),
            )
    return small.resize((size, size), Image.BICUBIC)


def mark(size, radius_ratio=0.234):
    """The rounded-square app mark: gradient tile, S glyph, accent slash."""
    s = size * SS
    tile = gradient(s, GREEN, BLUE).convert("RGBA")

    mask = Image.new("L", (s, s), 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, s - 1, s - 1],
                                          radius=int(s * radius_ratio), fill=255)
    tile.putalpha(mask)

    d = ImageDraw.Draw(tile)

    # A single centred S. An earlier version had a diagonal accent stroke behind
    # it, but the two shapes merged into an unreadable glyph once scaled to a
    # 16px favicon, so the mark is deliberately one letterform.
    f = font("Poppins-Bold.ttf", int(s * .60))
    box = d.textbbox((0, 0), "S", font=f)
    d.text(((s - (box[2] - box[0])) / 2 - box[0], (s - (box[3] - box[1])) / 2 - box[1]),
           "S", font=f, fill=INK)

    return tile.resize((size, size), Image.LANCZOS)


def wordmark(height=120, on_dark=True, transparent=True):
    """Full horizontal lockup: mark + SVED + dot + SEO."""
    h = height * SS
    m = int(h * .78)
    gap = int(h * .20)

    f_name = font("Poppins-Bold.ttf", int(h * .52))
    f_sub = font("Poppins-Medium.ttf", int(h * .30))

    probe = ImageDraw.Draw(Image.new("RGB", (10, 10)))
    w_name = probe.textbbox((0, 0), "SVED", font=f_name)[2]
    w_sub = probe.textbbox((0, 0), "SEO", font=f_sub)[2]
    dot_r = int(h * .075)

    total = m + gap + w_name + gap + dot_r * 2 + int(gap * .8) + w_sub + gap
    img = Image.new("RGBA", (total, h),
                    (0, 0, 0, 0) if transparent else ((NAVY + (255,)) if on_dark else (WHITE + (255,))))

    img.alpha_composite(mark(m), (0, (h - m) // 2))
    d = ImageDraw.Draw(img)

    text_col = WHITE if on_dark else INK
    x = m + gap
    bb = d.textbbox((0, 0), "SVED", font=f_name)
    d.text((x - bb[0], (h - (bb[3] - bb[1])) / 2 - bb[1]), "SVED", font=f_name, fill=text_col)

    x += w_name + gap
    cy = h // 2
    d.ellipse([x, cy - dot_r, x + dot_r * 2, cy + dot_r], fill=GREEN)

    x += dot_r * 2 + int(gap * .8)
    bb = d.textbbox((0, 0), "SEO", font=f_sub)
    d.text((x - bb[0], (h - (bb[3] - bb[1])) / 2 - bb[1]), "SEO", font=f_sub, fill=MUTED)

    return img.resize((total // SS, height), Image.LANCZOS)


def main():
    os.makedirs(BRAND, exist_ok=True)
    made = []

    # --- favicons -> assets/ (referenced by the site) ---
    for size in (16, 32, 48, 180, 192, 512):
        name = f"favicon-{size}.png" if size < 180 else (
            "apple-touch-icon.png" if size == 180 else f"icon-{size}.png")
        p = os.path.join(ASSETS, name)
        mark(size).save(p)
        made.append(p)

    ico = os.path.join(ASSETS, "favicon.ico")
    mark(256).save(ico, sizes=[(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)])
    made.append(ico)

    # --- brand pack -> brand/ (for decks, invoices, directories) ---
    for h, tag in ((120, "small"), (240, "medium"), (480, "large")):
        for dark, trans, suffix in ((True, True, "on-transparent"),
                                    (True, False, "on-dark"),
                                    (False, False, "on-light")):
            p = os.path.join(BRAND, f"sved-logo-{tag}-{suffix}.png")
            wordmark(h, on_dark=dark, transparent=trans).save(p)
            made.append(p)

    for size in (256, 512, 1024):
        p = os.path.join(BRAND, f"sved-mark-{size}.png")
        mark(size).save(p)
        made.append(p)

    for p in made:
        print(f"{os.path.getsize(p):>8,} bytes  {os.path.relpath(p, ROOT)}")
    print(f"\n{len(made)} files written")


if __name__ == "__main__":
    main()
