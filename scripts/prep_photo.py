"""Prepare Muzaki's red-background portrait for monochrome ASCII conversion."""
from pathlib import Path
import sys

from PIL import Image, ImageEnhance, ImageFilter, ImageOps

ROOT = Path(__file__).resolve().parent.parent
SOURCE = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "source-photo.png"
OUTPUT = Path(sys.argv[2]) if len(sys.argv) > 2 else ROOT / "source-prepped.png"

image = Image.open(SOURCE).convert("RGB")
pixels = image.load()
mask = Image.new("L", image.size, 0)
mask_pixels = mask.load()

for y in range(image.height):
    for x in range(image.width):
        red, green, blue = pixels[x, y]
        background_strength = red - max(green, blue)
        mask_pixels[x, y] = 0 if red > 95 and background_strength > 42 else 255

mask = mask.filter(ImageFilter.GaussianBlur(1.2))
gray = ImageEnhance.Brightness(ImageOps.grayscale(image)).enhance(0.82)
gray = ImageEnhance.Contrast(gray).enhance(1.08)
gray = ImageEnhance.Sharpness(gray).enhance(1.2)
prepared = Image.new("L", image.size, 255)
prepared.paste(gray, mask=mask)
prepared.save(OUTPUT)
print(f"wrote {OUTPUT} ({prepared.width}x{prepared.height})")
