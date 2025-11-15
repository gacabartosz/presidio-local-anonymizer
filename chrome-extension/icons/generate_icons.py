#!/usr/bin/env python3
"""
Generate PNG icons from SVG source
Requires: pip install cairosvg pillow
"""

import sys
import os

try:
    import cairosvg
    from PIL import Image
    import io
except ImportError:
    print("Installing required packages...")
    os.system(f"{sys.executable} -m pip install cairosvg pillow --user")
    import cairosvg
    from PIL import Image
    import io

# Icon sizes needed for Chrome extension
SIZES = [16, 32, 48, 128]

def generate_png(svg_path, size, output_path):
    """Convert SVG to PNG at specified size"""
    print(f"Generating {size}x{size} icon...")

    # Convert SVG to PNG bytes
    png_bytes = cairosvg.svg2png(
        url=svg_path,
        output_width=size,
        output_height=size
    )

    # Save to file
    with open(output_path, 'wb') as f:
        f.write(png_bytes)

    print(f"✓ Saved: {output_path}")

def main():
    # Get script directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    svg_path = os.path.join(script_dir, 'icon.svg')

    if not os.path.exists(svg_path):
        print(f"Error: {svg_path} not found!")
        sys.exit(1)

    print("=" * 50)
    print("Generating Chrome Extension Icons")
    print("=" * 50)

    # Generate all sizes
    for size in SIZES:
        output_path = os.path.join(script_dir, f'icon-{size}.png')
        generate_png(svg_path, size, output_path)

    print("=" * 50)
    print("✓ All icons generated successfully!")
    print("=" * 50)

if __name__ == '__main__':
    main()
