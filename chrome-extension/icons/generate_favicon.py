#!/usr/bin/env python3
"""
Generate favicon.ico from SVG source
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

def generate_favicon(svg_path, output_path):
    """Generate multi-size favicon.ico"""
    print("Generating favicon.ico with sizes: 16x16, 32x32, 48x48...")

    # Generate PNG images at different sizes
    sizes = [16, 32, 48]
    images = []

    for size in sizes:
        print(f"  Creating {size}x{size}...")
        png_bytes = cairosvg.svg2png(
            url=svg_path,
            output_width=size,
            output_height=size
        )
        img = Image.open(io.BytesIO(png_bytes))
        images.append(img)

    # Save as multi-size .ico
    print(f"Saving to {output_path}...")
    images[0].save(
        output_path,
        format='ICO',
        sizes=[(16, 16), (32, 32), (48, 48)],
        append_images=images[1:]
    )

    print("✓ Favicon generated successfully!")

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    svg_path = os.path.join(script_dir, 'icon.svg')

    # Generate for web-ui (go up 2 levels from icons/ to project root, then to web-ui/)
    project_root = os.path.dirname(os.path.dirname(script_dir))
    web_ui_dir = os.path.join(project_root, 'web-ui')
    favicon_path = os.path.join(web_ui_dir, 'favicon.ico')

    if not os.path.exists(svg_path):
        print(f"Error: {svg_path} not found!")
        sys.exit(1)

    print("=" * 50)
    print("Generating Favicon")
    print("=" * 50)

    generate_favicon(svg_path, favicon_path)

    print("=" * 50)

if __name__ == '__main__':
    main()
