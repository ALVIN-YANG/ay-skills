#!/usr/bin/env python3
"""Deterministic test renderer; the supplied raster remains a proportional layer."""

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont


root = Path(__file__).resolve().parent
source = Image.open(root / "raw-ui.ppm").convert("RGB")
canvas = Image.new("RGB", (2880, 1800), "#0b1220")
draw = ImageDraw.Draw(canvas)
font = ImageFont.load_default(size=96)
draw.text((220, 150), "See network quality", fill="#f8fafc", font=font)
draw.text((224, 280), "Release build 42 - fictional data", fill="#94a3b8", font=ImageFont.load_default(size=38))
target = (1920, 1120)
source.thumbnail(target, Image.Resampling.NEAREST)
frame = Image.new("RGB", (source.width + 36, source.height + 36), "#334155")
frame.paste(source, (18, 18))
canvas.paste(frame, ((canvas.width - frame.width) // 2, 500))
output = root / "output" / "en-US"
output.mkdir(parents=True, exist_ok=True)
canvas.save(output / "01-quality.png", format="PNG", optimize=True)
