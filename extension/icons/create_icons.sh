#!/bin/bash
# Create placeholder icons using ImageMagick or Python PIL

# Check if convert (ImageMagick) is available
if command -v convert &> /dev/null; then
  convert -size 16x16 xc:#2196F3 -pointsize 12 -fill white -gravity center -annotate +0+0 "P" icon16.png
  convert -size 48x48 xc:#2196F3 -pointsize 36 -fill white -gravity center -annotate +0+0 "P" icon48.png
  convert -size 128x128 xc:#2196F3 -pointsize 96 -fill white -gravity center -annotate +0+0 "P" icon128.png
  echo "Icons created with ImageMagick"
else
  # Fallback: Create with Python PIL
  python3 << 'PYTHON'
from PIL import Image, ImageDraw, ImageFont

for size in [16, 48, 128]:
    img = Image.new('RGB', (size, size), color='#2196F3')
    draw = ImageDraw.Draw(img)
    
    # Draw white "P"
    font_size = int(size * 0.6)
    try:
        font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", font_size)
    except:
        font = ImageFont.load_default()
    
    text = "P"
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    position = ((size - text_width) // 2, (size - text_height) // 2 - 2)
    draw.text(position, text, fill='white', font=font)
    
    img.save(f'icon{size}.png')

print("Icons created with Python PIL")
PYTHON
fi
