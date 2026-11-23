"""Share images (og:image, 1200x630) for every page of this site.

build.py's page() calls og_image(name, title, DOMAIN): writes assets/og/<name>.jpg only when
the title changes (hash cache in assets/og/.cache.json) and returns the public URL.
Original artwork drawn with Pillow (gradient + brand shape + title); no third-party images.
"""
import hashlib
import json
import os
import re

from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "assets", "og")
CACHE = os.path.join(OUT, ".cache.json")
FONT_DIR = "/usr/share/fonts/opentype/inter"
W, H = 1200, 630
V = "1"

BRAND = {'name': 'PADEL GLASS BOX', 'tag': 'Padel tools and guides', 'domain_label': 'padelglassbox.com', 'c1': '#0e2468', 'c2': '#1f5fd6', 'accent': '#e6ff3a', 'text': '#ffffff', 'suffix': '\\s*\\|\\s*Padel Glass Box\\s*$', 'home_title': 'Free padel tools, rules and guides for new players', 'shape': 'ball'}


def _font(name, size):
    for f in (os.path.join(FONT_DIR, name), os.path.join(FONT_DIR, "Inter-Bold.otf")):
        if os.path.exists(f):
            return ImageFont.truetype(f, size)
    return ImageFont.load_default()


def _hex(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def _background():
    b = BRAND
    c1, c2, ac = _hex(b["c1"]), _hex(b["c2"]), _hex(b["accent"])
    img = Image.new("RGB", (W, H))
    d = ImageDraw.Draw(img)
    for y in range(H):
        t = y / (H - 1)
        d.line([(0, y), (W, y)], fill=tuple(int(c1[i] + (c2[i] - c1[i]) * t) for i in range(3)))
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ld = ImageDraw.Draw(layer)
    shape = b.get("shape", "circle")
    if shape == "ball":  # padel ball with seam
        ld.ellipse([800, 150, 1130, 480], fill=ac + (255,))
        ld.arc([700, 120, 1000, 510], 300, 60, fill=(255, 255, 255, 230), width=10)
        ld.arc([930, 120, 1230, 510], 120, 240, fill=(255, 255, 255, 230), width=10)
    elif shape == "board":  # split-flap departure tiles
        for r in range(4):
            for c in range(5):
                x, y = 760 + c * 82, 150 + r * 92
                ld.rounded_rectangle([x, y, x + 70, y + 80], 8, fill=(255, 255, 255, 18 if (r + c) % 3 else 40))
                ld.line([(x, y + 40), (x + 70, y + 40)], fill=(0, 0, 0, 120), width=3)
        ld.rounded_rectangle([760, 150 + 92, 760 + 70, 230 + 92], 8, fill=ac + (255,))
    elif shape == "pitch":  # cricket pitch strip + stumps
        ld.rounded_rectangle([880, 60, 1020, 600], 10, fill=ac + (60,))
        for x in (925, 950, 975):
            ld.rectangle([x - 4, 120, x + 4, 230], fill=(255, 255, 255, 230))
            ld.rectangle([x - 4, 440, x + 4, 550], fill=(255, 255, 255, 230))
        ld.line([(880, 250), (1020, 250)], fill=(255, 255, 255, 200), width=4)
        ld.line([(880, 420), (1020, 420)], fill=(255, 255, 255, 200), width=4)
        ld.ellipse([1040, 300, 1110, 370], fill=(200, 30, 50, 255))
    elif shape == "yarn":  # yarn ball
        ld.ellipse([820, 160, 1120, 460], fill=ac + (255,))
        for k in range(-5, 6):
            ld.arc([820 + k * 14, 160, 1120 + k * 14, 460], 200, 340, fill=(255, 255, 255, 90), width=4)
        ld.line([(840, 420), (760, 560), (620, 590)], fill=ac + (255,), width=6)
    else:
        ld.ellipse([820, 140, 1140, 460], fill=ac + (255,))
    glow = layer.filter(ImageFilter.GaussianBlur(24))
    img.paste(glow, (0, 0), glow)
    img.paste(layer, (0, 0), layer)
    return img


_BG = None


def _wrap(d, text, font, maxw):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=font) <= maxw:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def _draw(title, path):
    global _BG
    if _BG is None:
        _BG = _background()
    b = BRAND
    img = _BG.copy()
    d = ImageDraw.Draw(img)
    ac, tx = _hex(b["accent"]), _hex(b.get("text", "#ffffff"))
    d.text((64, 56), b["name"], font=_font("InterDisplay-Black.otf", 34), fill=ac)
    d.text((64, 98), b["tag"], font=_font("Inter-SemiBold.otf", 26), fill=tx)
    size, lines, f = 74, [], None
    while size >= 44:
        f = _font("InterDisplay-Black.otf", size)
        lines = _wrap(d, title, f, 680)
        if len(lines) <= 4:
            break
        size -= 6
    y = 170 + max(0, (4 - len(lines))) * size * 0.28
    for ln in lines[:4]:
        d.text((64, y), ln, font=f, fill=tx)
        y += size * 1.12
    d.text((64, H - 70), b["domain_label"], font=_font("Inter-Bold.otf", 28), fill=ac)
    img.save(path, "JPEG", quality=80, optimize=True, progressive=True)


def og_image(file, title, domain):
    os.makedirs(OUT, exist_ok=True)
    name = file.replace(".html", "").replace("/", "-").strip("-") or "index"
    clean = re.sub(BRAND["suffix"], "", title).strip()
    if name == "index":
        clean = BRAND["home_title"]
    key = hashlib.md5((V + json.dumps(BRAND, sort_keys=True) + clean).encode()).hexdigest()
    try:
        cache = json.load(open(CACHE))
    except Exception:
        cache = {}
    path = os.path.join(OUT, name + ".jpg")
    if cache.get(name) != key or not os.path.exists(path):
        _draw(clean, path)
        cache[name] = key
        json.dump(cache, open(CACHE, "w"), indent=0, sort_keys=True)
    return f"{domain}/assets/og/{name}.jpg?v={key[:8]}"
