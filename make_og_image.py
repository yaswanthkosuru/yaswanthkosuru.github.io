#!/usr/bin/env python3
"""Generate assets/og-image.jpg — the 1200x630 social share card.

Composites the hero photo on the right over the site's dark theme, with the
name, role and tagline on the left. Re-run after changing the photo or copy.
"""
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H = 1200, 630
BG = (10, 10, 11)          # #0A0A0B — site background
FG = (255, 255, 255)
ACCENT = (196, 245, 66)    # #C4F542 — site accent green
MUTED = (255, 255, 255)

BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
MONO = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"

img = Image.new("RGB", (W, H), BG)

# ---- right: hero photo, cover-cropped to the right 40%, faded into the bg ----
photo = Image.open("assets/yaswanth.jpg").convert("RGB")
PW = 460
scale = H / photo.height if photo.width / photo.height > PW / H else PW / photo.width
pw, ph = round(photo.width * scale), round(photo.height * scale)
photo = photo.resize((pw, ph), Image.LANCZOS)
photo = photo.crop(((pw - PW) // 2, (ph - H) // 4, (pw - PW) // 2 + PW, (ph - H) // 4 + H))
img.paste(photo, (W - PW, 0))

# left-edge gradient over the photo so text side blends into it
fade = Image.new("L", (PW, 1), 0)
for x in range(PW):
    t = x / PW
    fade.putpixel((x, 0), round(255 * max(0.0, 1 - t * 2.2)))  # opaque -> clear by ~45%
fade = fade.resize((PW, H))
img.paste(Image.new("RGB", (PW, H), BG), (W - PW, 0), fade)
# slight overall darken so white text never fights the photo
shade = Image.new("L", (PW, H), 60)
img.paste(Image.new("RGB", (PW, H), BG), (W - PW, 0), shade)

# ---- soft accent glow top-left (echoes the site's radial glow) ----
glow = Image.new("RGB", (W, H), BG)
gd = ImageDraw.Draw(glow)
gd.ellipse([-350, -350, 500, 380], fill=(28, 34, 13))
glow = glow.filter(ImageFilter.GaussianBlur(160))
img = Image.blend(img, glow, 0.35)

d = ImageDraw.Draw(img)

# ---- left: copy ----
X = 84
d.rectangle([X, 96, X + 46, 100], fill=ACCENT)
d.text((X, 120), "FULL-STACK ENGINEER — AI · REAL-TIME · CLOUD",
       font=ImageFont.truetype(MONO, 22), fill=ACCENT)

name = ImageFont.truetype(BOLD, 104)
d.text((X - 6, 176), "YASWANTH", font=name, fill=FG)
d.text((X - 6, 288), "KOSURU", font=name, fill=FG)

tag = ImageFont.truetype(SANS, 28)
d.text((X, 436), "0-to-1 platforms, event-driven services", font=tag, fill=(190, 190, 192))
d.text((X, 476), "and production LLM pipelines.", font=tag, fill=(190, 190, 192))

d.text((X, 556), "yaswanthkosuru.github.io", font=ImageFont.truetype(MONO, 22),
       fill=(140, 140, 144))

# thin border like the site's cards
d.rectangle([0, 0, W - 1, H - 1], outline=(50, 50, 53), width=2)

img.save("assets/og-image.jpg", "JPEG", quality=90)
print("wrote assets/og-image.jpg", img.size)
