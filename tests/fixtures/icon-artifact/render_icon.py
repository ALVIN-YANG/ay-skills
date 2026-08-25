#!/usr/bin/env python3
"""Create the approved deterministic icon fixture as an opaque PNG."""

from pathlib import Path
from PIL import Image, ImageDraw


root = Path(__file__).resolve().parent
image = Image.new("RGB", (1024, 1024), "#f2eadf")
draw = ImageDraw.Draw(image)
draw.rounded_rectangle((132, 132, 892, 892), radius=180, fill="#183a37")
draw.ellipse((292, 250, 732, 690), fill="#f4b860")
draw.polygon(((512, 310), (655, 610), (512, 545), (369, 610)), fill="#f2eadf")
draw.ellipse((454, 700, 570, 816), fill="#d95d39")
output = root / "output"
output.mkdir(exist_ok=True)
image.save(output / "AppIcon-1024.png", format="PNG", optimize=True)
