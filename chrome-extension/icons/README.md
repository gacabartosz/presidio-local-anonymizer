# Extension Icons

This directory contains the icons for the Presidio Browser Anonymizer Chrome extension.

## Files

- **icon.svg** - Source SVG file (200x200, fills entire square)
- **icon-16.png** - 16x16 toolbar icon
- **icon-32.png** - 32x32 toolbar icon
- **icon-48.png** - 48x48 extension management icon
- **icon-128.png** - 128x128 Chrome Web Store icon
- **generate_icons.py** - Script to generate PNG icons from SVG
- **generate_favicon.py** - Script to generate favicon.ico for web dashboard

## Regenerating Icons

If you modify `icon.svg`, regenerate the PNG icons:

```bash
cd chrome-extension/icons
python3 generate_icons.py
```

This will regenerate all PNG sizes (16, 32, 48, 128).

## Regenerating Favicon

To regenerate the favicon for the web dashboard:

```bash
cd chrome-extension/icons
python3 generate_favicon.py
```

This will create `web-ui/favicon.ico` with embedded 16x16, 32x32, and 48x48 sizes.

## Design

The icon features:
- **Blue gradient background** - Fills entire 200x200 square
- **Shield symbol** - Represents security and protection
- **Lock** - Privacy and data security
- **Corner accents** - Modern tech aesthetic
- **No empty margins** - Maximizes visibility in small sizes

## Requirements

```bash
pip install cairosvg pillow
```

The scripts will auto-install these if missing.
