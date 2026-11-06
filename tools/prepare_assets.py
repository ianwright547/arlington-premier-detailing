"""One-time asset prep: downloads generated photos, cuts the logo set, makes the OG card and icons."""
import io, os, re, sys, urllib.request
import numpy as np
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
A = os.path.join(ROOT, "public", "assets")
I = os.path.join(A, "img")
os.makedirs(I, exist_ok=True)
BASE = "https://d8j0ntlcm91z4.cloudfront.net/user_3BmwgpjErpTVpPqbaM1cAWqXcuF/"
PHOTOS = {
    "hero": "hf_20261106_194641_d83e0b32-c0f2-45ad-b4dc-cbc9aee6e450",
    "foam": "hf_20261106_194530_81fc517c-7dfc-4eac-84b0-5dc2e9b91244",
    "interior": "hf_20261106_194530_8e8dfb74-d3a7-4383-a8c3-a5a57e171418",
    "polish": "hf_20261106_194529_8dce2bf0-b48f-46c2-b90d-191d1e240d47",
    "seats": "hf_20261106_194642_1f76f225-32d8-4a63-ad36-628d3654a2f0",
    "wheel": "hf_20261106_194531_718146e3-e156-429d-bcaf-22fcd09085ea",
    "pethair": "hf_20261106_194531_2e960336-134a-4c29-8623-18ab6abee0ce",
    "seat": "hf_20261106_194531_9d53cc41-7b69-4503-b691-7fda40a1b7af",
    "carpet": "hf_20261106_194530_d29ee55a-875e-4908-ab44-061a271b4d4e",
    "engine": "hf_20261106_194640_9547ed17-98c1-4bdc-9256-6ddb4724a14b",
    "headlight": "hf_20261106_194530_016a5d48-ae24-4faa-b3c0-ff935b302c35",
    "clay": "hf_20261106_194734_ce41c9b8-a2ba-4f27-8e97-5094f2bdc621",
    "wax": "hf_20261106_194735_0da7eae0-3b07-4d6c-bcee-9914f7da1b8c",
    "beads": "hf_20261106_194735_3a14dac9-3132-4a50-a18b-85ec4349e38a",
    "wheelseal": "hf_20261106_194735_567a7609-7791-4da6-8322-c9a98eb6262a",
    "paint": "hf_20261106_194642_ab9f97a3-9cf6-45f1-afff-2b21d4aece33",
}
zipdir, tabdir = sys.argv[1], sys.argv[2]

for name, key in PHOTOS.items():
    dst = os.path.join(I, name + ".jpg")
    if os.path.exists(dst):
        continue
    req = urllib.request.Request(BASE + key + ".png", headers={"User-Agent": "Mozilla/5.0"})
    im = Image.open(io.BytesIO(urllib.request.urlopen(req, timeout=120).read())).convert("RGB")
    w = 1920 if name in ("hero", "paint") else 1200
    if im.width > w:
        im = im.resize((w, round(im.height * w / im.width)), Image.LANCZOS)
    im.save(dst, quality=82, optimize=True, progressive=True)
    print(name, im.size, os.path.getsize(dst) // 1024, "KB")

Image.open(os.path.join(tabdir, "shop-front.jpg")).convert("RGB").save(os.path.join(I, "shop-front.jpg"), quality=82)

logo = Image.open(os.path.join(zipdir, "DF617D10-5F8E-44CA-B9C0-F197C66C8B96.png")).convert("RGB")
print("logo", logo.size)
s = logo.width / 1774


def key_black(im):
    a = np.asarray(im).astype(float)
    m = a.max(axis=2)
    alpha = np.clip((m - 14) * 2.0, 0, 255)
    rgba = np.dstack([a, alpha]).astype("uint8")
    return Image.fromarray(rgba, "RGBA")


def box(x0, y0, x1, y1):
    return tuple(round(v * s) for v in (x0, y0, x1, y1))


full = key_black(logo.crop(box(90, 50, 1690, 640)))
full.save(os.path.join(A, "logo-full.png"), optimize=True)
navl = full.resize((564, round(564 * full.height / full.width)), Image.LANCZOS)
navl.save(os.path.join(A, "logo-nav.png"), optimize=True)
print("nav", navl.size)
for k, b in {"cleaner": (345, 635, 490, 775), "protected": (655, 635, 800, 775), "brighter": (982, 635, 1125, 775), "lasting": (1293, 635, 1436, 775)}.items():
    key_black(logo.crop(box(*b))).resize((168, 168), Image.LANCZOS).save(os.path.join(A, f"icon-{k}.png"), optimize=True)

BG = (5, 8, 13)
card = Image.new("RGB", (800, 800), BG)
c = full.resize((720, round(720 * full.height / full.width)), Image.LANCZOS)
card.paste(c, (40, (800 - c.height) // 2), c)
card.save(os.path.join(A, "logo-card.png"), optimize=True)

mark = key_black(logo.crop(box(300, 60, 1610, 390)))
sq = Image.new("RGB", (512, 512), BG)
m = mark.resize((472, round(472 * mark.height / mark.width)), Image.LANCZOS)
sq.paste(m, (20, (512 - m.height) // 2), m)
sq.resize((192, 192), Image.LANCZOS).save(os.path.join(A, "icon-192.png"), optimize=True)
sq.resize((180, 180), Image.LANCZOS).save(os.path.join(A, "apple-touch-icon.png"), optimize=True)
sq.save(os.path.join(ROOT, "public", "favicon.ico"), sizes=[(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)])

hero = Image.open(os.path.join(I, "hero.jpg"))
r = max(1200 / hero.width, 630 / hero.height)
h = hero.resize((round(hero.width * r), round(hero.height * r)), Image.LANCZOS)
h = h.crop(((h.width - 1200) // 2, (h.height - 630) // 2, (h.width + 1200) // 2, (h.height + 630) // 2)).convert("RGBA")
shade = Image.new("RGBA", (1200, 630), (0, 0, 0, 0))
d = ImageDraw.Draw(shade)
for x in range(800):
    d.line([(x, 0), (x, 630)], fill=(3, 6, 10, int(235 * (1 - x / 800) ** 0.7)))
h = Image.alpha_composite(h, shade)
ol = full.resize((640, round(640 * full.height / full.width)), Image.LANCZOS)
h.alpha_composite(ol, (36, 40))
d = ImageDraw.Draw(h)
f = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 34)
f2 = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 26)
d.text((58, 340), "Professional Detailing", font=f, fill=(255, 255, 255))
d.text((58, 386), "Inside and Out", font=f, fill=(90, 180, 245))
d.text((58, 450), "Arlington, VA  |  (703) 243-3080", font=f2, fill=(225, 232, 240))
h.convert("RGB").save(os.path.join(A, "og-card-v1.jpg"), quality=85)
print("done")
