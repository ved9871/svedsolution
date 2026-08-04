# -*- coding: utf-8 -*-
"""
Social profile pictures and cover banners for SVED Solution.

    python tools/make_social.py

Sizes and safe zones follow each platform's current spec:

  Facebook page cover   1640x624   mobile crops to the centre ~1160px
  LinkedIn company      2256x382   page logo overlaps the lower-left corner
  X header              1500x500   avatar overlaps lower-left, UI overlays right
  Reddit banner         1920x384   community icon overlaps the left
  Quora space           1280x320
  YouTube channel art   2560x1440  only the centre 1546x423 is always visible

Profile images are drawn with generous padding because every platform crops
them to a circle.
"""
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONTS = os.path.join(ROOT, ".fonts")
OUT = os.path.join(ROOT, "brand", "social")

GREEN = (0, 255, 178)
BLUE = (0, 165, 255)
INK = (7, 12, 18)
NAVY = (11, 18, 25)
LINE = (26, 37, 48)
WHITE = (255, 255, 255)
MUTED = (132, 150, 169)
FAINT = (92, 110, 128)

URL = "svedsolution.com"
HEADLINE = "Google ranks pages. AI recommends brands."
SUBLINE = "AI Visibility \u00b7 GEO \u00b7 AEO \u00b7 LLM SEO"


def font(name, size):
    p = os.path.join(FONTS, name)
    if os.path.exists(p):
        return ImageFont.truetype(p, size)
    win = os.path.join(os.environ.get("WINDIR", "C:/Windows"), "Fonts")
    for fb in ("segoeuib.ttf", "arialbd.ttf", "arial.ttf"):
        q = os.path.join(win, fb)
        if os.path.exists(q):
            return ImageFont.truetype(q, size)
    return ImageFont.load_default()


def w_of(draw, text, f):
    b = draw.textbbox((0, 0), text, font=f)
    return b[2] - b[0]


def gradient_square(size, a=GREEN, b=BLUE, steps=160):
    small = Image.new("RGB", (steps, steps))
    px = small.load()
    d = max(steps - 1, 1)
    for y in range(steps):
        for x in range(steps):
            t = (x + y) / (2 * d)
            px[x, y] = (int(a[0] + (b[0] - a[0]) * t),
                        int(a[1] + (b[1] - a[1]) * t),
                        int(a[2] + (b[2] - a[2]) * t))
    return small.resize((size, size), Image.BICUBIC)


def mark(size, radius_ratio=0.234):
    """
    Gradient tile with a centred S.

    radius_ratio=0 gives a full-bleed square, which is what avatars need:
    every platform crops them to a circle, and rounded corners flattened to
    RGB would leave black wedges outside the crop on any platform that does
    not.
    """
    ss = 4
    s = size * ss
    tile = gradient_square(s).convert("RGBA")
    if radius_ratio > 0:
        m = Image.new("L", (s, s), 0)
        ImageDraw.Draw(m).rounded_rectangle([0, 0, s - 1, s - 1],
                                            radius=int(s * radius_ratio), fill=255)
        tile.putalpha(m)
    d = ImageDraw.Draw(tile)
    f = font("Poppins-Bold.ttf", int(s * .60))
    bb = d.textbbox((0, 0), "S", font=f)
    d.text(((s - (bb[2] - bb[0])) / 2 - bb[0], (s - (bb[3] - bb[1])) / 2 - bb[1]),
           "S", font=f, fill=INK)
    return tile.resize((size, size), Image.LANCZOS)


def backdrop(w, h):
    """Dark canvas with a faint grid and a green glow, matching the website."""
    img = Image.new("RGB", (w, h), NAVY)
    d = ImageDraw.Draw(img)

    step = max(int(h / 7), 28)
    for x in range(0, w, step):
        d.line([(x, 0), (x, h)], fill=LINE, width=1)
    for y in range(0, h, step):
        d.line([(0, y), (w, y)], fill=LINE, width=1)

    glow = Image.new("RGB", (max(w // 8, 8), max(h // 8, 8)), NAVY)
    gd = ImageDraw.Draw(glow)
    gw, gh = glow.size
    gd.ellipse([int(gw * .52), int(-gh * .55), int(gw * 1.25), int(gh * .85)], fill=(0, 62, 47))
    gd.ellipse([int(-gw * .18), int(gh * .45), int(gw * .40), int(gh * 1.5)], fill=(4, 30, 54))
    glow = glow.filter(ImageFilter.GaussianBlur(gw // 9)).resize((w, h), Image.BICUBIC)

    return Image.blend(img, glow, 0.55).convert("RGBA")


def banner(w, h, path, safe_left=0, safe_right=0, compact=None,
           headline=HEADLINE, subline=SUBLINE, show_url=True, center=False):
    img = backdrop(w, h)
    d = ImageDraw.Draw(img)

    if compact is None:
        compact = (w / h) > 4.2

    pad = int(h * (0.16 if not compact else 0.22))
    left = max(pad, safe_left)
    right = w - max(pad, safe_right)
    avail = right - left

    m = int(h * (0.30 if compact else 0.26))
    f_name = font("Poppins-Bold.ttf", int(m * .70))
    f_head = font("Poppins-SemiBold.ttf", int(h * (0.115 if compact else 0.105)))
    f_sub = font("Poppins-Medium.ttf", int(h * (0.075 if compact else 0.062)))
    f_url = font("Poppins-Medium.ttf", int(h * (0.072 if compact else 0.058)))

    if compact:
        # One horizontal band: mark + wordmark, divider, headline, url right.
        cy = h // 2
        img.alpha_composite(mark(m), (left, cy - m // 2))
        x = left + m + int(m * .34)
        bb = d.textbbox((0, 0), "SVED", font=f_name)
        d.text((x - bb[0], cy - (bb[3] - bb[1]) / 2 - bb[1]), "SVED", font=f_name, fill=WHITE)
        x += w_of(d, "SVED", f_name) + int(m * .34)
        d.ellipse([x, cy - int(m * .07), x + int(m * .14), cy + int(m * .07)], fill=GREEN)
        x += int(m * .14) + int(m * .40)

        d.line([(x, cy - m // 2), (x, cy + m // 2)], fill=(34, 48, 63), width=2)
        x += int(m * .42)

        # Reserve the url column, then fit the headline into what is left.
        # Sizing against a fixed fraction of the banner let the headline run
        # under the url on very wide canvases such as the LinkedIn cover.
        url_w = (w_of(d, URL, f_url) + int(h * .5)) if show_url else 0
        head_max = right - x - url_w
        while w_of(d, headline, f_head) > head_max and f_head.size > 10:
            f_head = font("Poppins-SemiBold.ttf", f_head.size - 2)

        bb = d.textbbox((0, 0), headline, font=f_head)
        d.text((x - bb[0], cy - (bb[3] - bb[1]) / 2 - bb[1]), headline, font=f_head, fill=MUTED)

        if show_url:
            uw = w_of(d, URL, f_url)
            bb = d.textbbox((0, 0), URL, font=f_url)
            d.text((right - uw - bb[0], cy - (bb[3] - bb[1]) / 2 - bb[1]), URL, font=f_url, fill=GREEN)
    else:
        while w_of(d, headline, f_head) > avail * 0.95 and f_head.size > 10:
            f_head = font("Poppins-SemiBold.ttf", f_head.size - 2)
        block_h = m + int(h * .10) + f_head.size + int(h * .05) + f_sub.size
        y = (h - block_h) // 2
        x0 = left + (avail - m) // 2 if center else left

        img.alpha_composite(mark(m), (x0, y))
        bb = d.textbbox((0, 0), "SVED", font=f_name)
        d.text((x0 + m + int(m * .32) - bb[0], y + (m - (bb[3] - bb[1])) / 2 - bb[1]),
               "SVED", font=f_name, fill=WHITE)

        y += m + int(h * .10)
        hx = left + (avail - w_of(d, headline, f_head)) // 2 if center else left
        bb = d.textbbox((0, 0), headline, font=f_head)
        d.text((hx - bb[0], y - bb[1]), headline, font=f_head, fill=WHITE)

        y += f_head.size + int(h * .05)
        sx = left + (avail - w_of(d, subline, f_sub)) // 2 if center else left
        bb = d.textbbox((0, 0), subline, font=f_sub)
        d.text((sx - bb[0], y - bb[1]), subline, font=f_sub, fill=GREEN)

        if show_url:
            uw = w_of(d, URL, f_url)
            bb = d.textbbox((0, 0), URL, font=f_url)
            # Centred layouts put the url on the centre line under the subline.
            # Bottom-right crowded the subline on shorter canvases.
            ux = left + (avail - uw) // 2 if center else right - uw
            uy = max(y + f_sub.size + int(h * .09), h - pad - f_url.size)
            d.text((ux - bb[0], uy - bb[1]), URL, font=f_url, fill=FAINT)

    img.convert("RGB").save(path, quality=95)
    return path


def profile(size, path, pad_ratio=0.0):
    """Square avatar. Full-bleed gradient, since platforms crop to a circle."""
    if pad_ratio <= 0:
        mark(size, radius_ratio=0).convert("RGB").save(path)
        return path
    # Padded variant: navy field with the rounded mark inset, for anywhere the
    # image is shown as a square.
    img = Image.new("RGBA", (size, size), NAVY + (255,))
    inner = int(size * (1 - pad_ratio * 2))
    img.alpha_composite(mark(inner), ((size - inner) // 2, (size - inner) // 2))
    img.convert("RGB").save(path)
    return path


def main():
    os.makedirs(OUT, exist_ok=True)
    made = []

    # ---- profile pictures ------------------------------------------------
    for size, name in [(1080, "profile-master-1080.png"), (400, "profile-x-quora-400.png"),
                       (300, "profile-linkedin-300.png"), (256, "profile-reddit-256.png"),
                       (180, "profile-facebook-180.png"), (320, "profile-instagram-320.png")]:
        made.append(profile(size, os.path.join(OUT, name)))

    # Padded variant for platforms that crop tightly to a circle.
    made.append(profile(1080, os.path.join(OUT, "profile-master-1080-padded.png"), pad_ratio=0.10))

    # ---- cover banners ---------------------------------------------------
    made.append(banner(1640, 624, os.path.join(OUT, "cover-facebook-1640x624.png"),
                       safe_left=250, safe_right=250, center=True))
    made.append(banner(2256, 382, os.path.join(OUT, "cover-linkedin-2256x382.png"),
                       safe_left=520))          # page logo overlaps lower-left
    made.append(banner(1500, 500, os.path.join(OUT, "cover-x-1500x500.png"),
                       safe_left=60, safe_right=60))
    made.append(banner(1920, 384, os.path.join(OUT, "cover-reddit-1920x384.png"),
                       safe_left=360))          # community icon overlaps left
    made.append(banner(1280, 320, os.path.join(OUT, "cover-quora-1280x320.png"),
                       safe_left=60, safe_right=60))
    made.append(banner(2560, 1440, os.path.join(OUT, "cover-youtube-2560x1440.png"),
                       safe_left=507, safe_right=507, center=True, compact=False))
    made.append(banner(1200, 630, os.path.join(OUT, "og-share-1200x630.png"),
                       safe_left=70, safe_right=70))
    made.append(banner(1080, 1080, os.path.join(OUT, "instagram-post-1080.png"),
                       safe_left=90, safe_right=90, compact=False, center=True))

    for p in made:
        im = Image.open(p)
        print("%-42s %5dx%-5d %8s" % (os.path.basename(p), im.width, im.height,
                                      f"{os.path.getsize(p) // 1024} KB"))
    print(f"\n{len(made)} files -> brand/social/")


if __name__ == "__main__":
    main()
