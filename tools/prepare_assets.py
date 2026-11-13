"""Legacy photo import. The site uses its checked-in logo files and make_social_cards.py for current branding."""
import io, os, sys, urllib.request
from PIL import Image

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
_, tabdir = sys.argv[1:3]  # Retain the original command-line argument positions.

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
