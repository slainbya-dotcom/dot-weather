"""Generates the app icons (PNG/ICO/ICNS) with Pillow: dot-matrix sun behind a cloud.
Run: python tools/make_icons.py   (or replace with `npx tauri icon your-1024.png`)"""
import math, os
from PIL import Image, ImageDraw

OUT = os.path.join(os.path.dirname(__file__), "..", "src-tauri", "icons")
S = 1024
N = 13                       # dot grid size
AMBER = (255, 176, 0)

def master():
    img = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    pad = 64
    d.rounded_rectangle([pad, pad, S - pad, S - pad], radius=200, fill=(20, 20, 22, 255))
    inner = S - 2 * pad - 120
    pitch = inner / N
    ox = oy = pad + 60
    c = (N - 1) // 2
    for gy in range(N):
        for gx in range(N):
            # Sun (amber, top right) behind a cloud (light grey, bottom left).
            cloud = ['0000000000000', '0000000000000', '0000000000000', '0000000000000', '0000000000000',
                     '0001110000000', '0011111110000', '0111111111000', '1111111111100', '1111111111100',
                     '0111111111000', '0000000000000', '0000000000000']
            in_cloud = cloud[gy][gx] == '1'
            in_sun = (gx - 8) ** 2 + (gy - 4) ** 2 <= 9 or (gy in (0, 8) and gx == 8) or (gx in (4, 12) and gy == 4)
            lit = in_cloud or in_sun
            r = pitch * 0.38
            x = ox + gx * pitch + pitch / 2
            y = oy + gy * pitch + pitch / 2
            col = (214, 218, 226, 255) if in_cloud else AMBER + (255,) if in_sun else (54, 42, 19, 255)
            d.ellipse([x - r, y - r, x + r, y + r], fill=col)
    return img

m = master()
os.makedirs(OUT, exist_ok=True)
for name, size in [("32x32.png", 32), ("128x128.png", 128), ("128x128@2x.png", 256), ("icon.png", 512)]:
    m.resize((size, size), Image.LANCZOS).save(os.path.join(OUT, name))
m.save(os.path.join(OUT, "icon.ico"), sizes=[(16, 16), (24, 24), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)])
m.save(os.path.join(OUT, "icon.icns"))
print("icons written to", os.path.abspath(OUT))
