"""
Alliston Tailoring & Alterations — Site Builder
Rebuilds index.html and services.html from source files with all images embedded as base64.
Run: python3 build.py
"""

import re, base64, os

img_dir = "assets/images"

def b64(path, mime):
    with open(path, "rb") as f:
        return b'src="data:' + mime.encode() + b";base64," + base64.b64encode(f.read()) + b'"'

def swap_gallery(m):
    name = m.group(1).decode()
    path = os.path.join(img_dir, name)
    return b64(path, "image/jpeg") if os.path.exists(path) else m.group(0)

def transform(h):
    # CSS Variables — dark to light
    h = h.replace(b"--bg:       #111110;",  b"--bg:       #FBF0E6;")
    h = h.replace(b"--bg-card:  #191614;",  b"--bg-card:  #F5E4D2;")
    h = h.replace(b"--bg-hover: #201D19;",  b"--bg-hover: #EDD7C5;")
    h = h.replace(b"--beige:    #CEC6BB;",  b"--beige:    #3A2418;")
    h = h.replace(b"--dim:      #6B6360;",  b"--dim:      #9B7B6E;")
    h = h.replace(b"--white:    #F0EBE4;",  b"--white:    #1A0A04;")

    # Body gradient
    h = h.replace(
        b"      background: var(--bg);\n      color: var(--beige);",
        b"      background: linear-gradient(155deg, #F8CBAB 0%, #FBF0E4 52%, #FEF7F0 100%);\n"
        b"      background-attachment: fixed;\n"
        b"      color: var(--beige);"
    )

    # Nav — light frosted glass
    h = h.replace(
        b"      background: rgba(29,29,27,.92); backdrop-filter: blur(10px);",
        b"      background: rgba(253,244,236,.93); backdrop-filter: blur(10px);"
    )

    # Border rgba — flip light to dark warm
    h = h.replace(b"rgba(205,198,190,", b"rgba(80,45,30,")
    h = h.replace(b"rgba(17,17,16,.55)", b"rgba(255,248,243,.78)")
    h = h.replace(b"rgba(29,29,27,.5)",  b"rgba(255,248,243,.5)")

    # Embed gallery images
    h = re.sub(rb'src="gallery/(photo_[^"]+)"', swap_gallery, h)

    # Embed logos
    h = h.replace(b'src="logo.jpg"',         b64("assets/logo.jpg", "image/jpeg"))
    h = h.replace(b'src="logo_graphic.png"', b64("assets/logo_graphic.png", "image/png"))

    return h

# ── Build index.html ──────────────────────────────────────────────────────────
with open("source/index-original.html", "rb") as f:
    h = f.read()
h = transform(h)
with open("index.html", "wb") as f:
    f.write(h)
print(f"Built index.html ({os.path.getsize('index.html') // 1024} KB)")

# ── Build services.html ───────────────────────────────────────────────────────
with open("source/services-original.html", "rb") as f:
    h = f.read()
h = transform(h)
with open("services.html", "wb") as f:
    f.write(h)
print(f"Built services.html ({os.path.getsize('services.html') // 1024} KB)")

# ── Build about.html ──────────────────────────────────────────────────────────
with open("source/about-original.html", "rb") as f:
    h = f.read()
h = transform(h)
with open("about.html", "wb") as f:
    f.write(h)
print(f"Built about.html ({os.path.getsize('about.html') // 1024} KB)")
