#!/usr/bin/env python3
"""Build one branded 1200x630 social share card per page.

Run after generate.py: python tools/make_social_cards.py
Each card takes its headline and photo from the built page and is saved to
public/assets/og/. Cards carry no phone number or address, so changing those
does not mean rebuilding them.
"""
import glob, html, os, re, sys
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PUB = os.path.join(ROOT, "public")
OUT = os.path.join(PUB, "assets", "og")
W, H = 1200, 630
PAD = 56
BLUE = (30, 155, 240)
NAVY = (5, 8, 13)
SHORT = {"/": "Professional Auto Detailing"}


def font(size):
    try:
        f = ImageFont.truetype("bahnschrift.ttf", size)
        f.set_variation_by_name("Bold Condensed")
        return f
    except OSError:
        return ImageFont.truetype("Impact.ttf", size)


def cover(path):
    im = Image.open(path).convert("RGB")
    s = max(W / im.width, H / im.height)
    im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    x, y = (im.width - W) // 2, (im.height - H) // 2
    return im.crop((x, y, x + W, y + H))


def shade(im):
    """Dark on the left for the text, clear on the right for the photo."""
    a = Image.new("L", (W, 1))
    for x in range(W):
        t = min(1, x / (W * 0.82))
        a.putpixel((x, 0), round(248 * (1 - t ** 1.7) + 34))
    a = a.resize((W, H))
    return Image.composite(Image.new("RGB", (W, H), NAVY), im, a)


def wrap(draw, text, f, width):
    lines, cur = [], ""
    for w in text.split():
        t = f"{cur} {w}".strip()
        if draw.textlength(t, font=f) <= width:
            cur = t
        else:
            lines.append(cur)
            cur = w
    return lines + [cur]


def card(title, photo, dest):
    im = shade(cover(photo))
    d = ImageDraw.Draw(im)
    logo = Image.open(os.path.join(PUB, "assets", "logo-full.png")).convert("RGBA")
    lw = 320
    logo = logo.resize((lw, round(logo.height * lw / logo.width)), Image.LANCZOS)
    im.paste(logo, (PAD - 8, 34), logo)
    text = title.upper()
    for size in (92, 80, 70, 60, 52):
        f = font(size)
        lines = wrap(d, text, f, 660)
        if len(lines) <= 3 and all(lines):
            break
    lh = round(size * 1.12)
    y = H - PAD - 44 - lh * len(lines)
    for i, ln in enumerate(lines):
        d.text((PAD, y + i * lh), ln, font=f, fill="white")
    y2 = H - PAD - 26
    d.rectangle((PAD, y2 - 8, PAD + 64, y2 - 4), fill=BLUE)
    d.text((PAD, y2 + 2), "ARLINGTON, VA  |  BY TAB MOTORS", font=font(26), fill=BLUE)
    d.rectangle((0, H - 8, W, H), fill=BLUE)
    im.save(dest, "JPEG", quality=84, optimize=True, progressive=True)


def main():
    os.makedirs(OUT, exist_ok=True)
    n = 0
    for fp in glob.glob(os.path.join(PUB, "**", "index.html"), recursive=True):
        rel = os.path.relpath(os.path.dirname(fp), PUB).replace("\\", "/")
        path = "/" if rel == "." else f"/{rel}/"
        h = open(fp, encoding="utf-8").read()
        h1 = re.search(r"<h1[^>]*>(.*?)</h1>", h, re.S).group(1)
        title = SHORT.get(path, html.unescape(re.sub(r"<[^>]+>", " ", h1)))
        title = re.sub(r"\s+", " ", title).strip()
        img = re.search(r"/assets/img/([\w-]+\.jpg)", h[h.find("<main"):]).group(1)
        slug = path.strip("/").replace("/", "-") or "home"
        card(title, os.path.join(PUB, "assets", "img", img), os.path.join(OUT, slug + ".jpg"))
        n += 1
    print(n, "cards")


if __name__ == "__main__":
    sys.exit(main())
