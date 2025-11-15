# Presidio Browser Anonymizer - Chrome Extension

Chrome extension for real-time PII anonymization powered by Microsoft Presidio.

## Features

- **Real-time Anonymization**: Anonymize selected text with Ctrl+Shift+A
- **Context Menu**: Right-click selected text → "Anonimizuj zaznaczony tekst"
- **Configurable Backend**: Connect to any Presidio backend instance
- **Polish Language Support**: Optimized for Polish PII (PESEL, NIP, names, locations)
- **28 Entity Types**: Emails, phones, credit cards, IDs, and more

## Installation

### 1. Install Backend

```bash
# Clone repository
git clone https://github.com/gacabartosz/presidio-local-anonymizer
cd presidio-local-anonymizer/backend

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Download SpaCy model
python -m spacy download pl_core_news_md

# Run backend
python app.py
```

Backend will start on `http://localhost:4222`

### 2. Install Chrome Extension

#### Option A: Load Unpacked (Development)

1. Open Chrome → `chrome://extensions/`
2. Enable "Developer mode" (top-right corner)
3. Click "Load unpacked"
4. Select `/path/to/presidio-local-anonymizer/chrome-extension` folder

#### Option B: From GitHub Releases

1. Download latest `.crx` or `.zip` from [Releases](https://github.com/gacabartosz/presidio-local-anonymizer/releases)
2. Drag & drop into `chrome://extensions/`

## Configuration

### Setting Backend URL

1. Click extension icon
2. Click "🔧 Konfiguracja Wtyczki"
3. Enter backend URL (e.g., `http://localhost:4222`)
4. Click "🔍 Testuj Połączenie" to verify
5. Click "💾 Zapisz" to save

### Custom Port or Host

If you run backend on different port:

```bash
python app.py --port 8080
```

Then update extension config:
- Open extension options
- Set URL to `http://localhost:8080`
- Save

## Usage

### Auto-Anonymize on Paste (NEW!)

**Automatic anonymization when you paste text anywhere:**

1. Copy text containing PII (e.g., email, PESEL, phone number)
2. Paste it anywhere with `Ctrl+V` (or `Cmd+V` on Mac)
3. Text will be **automatically anonymized** before insertion!

Works everywhere:
- ChatGPT and other AI chatbots
- Email clients (Gmail, Outlook)
- Forms and text fields
- Content-editable areas

### Keyboard Shortcut

1. Select text on any webpage
2. Press `Ctrl+Shift+A` (or `Cmd+Shift+A` on Mac)
3. Text will be anonymized instantly

### Context Menu

1. Select text
2. Right-click
3. Choose "Anonimizuj zaznaczony tekst"

### Dashboard

- Click extension icon → "⚙️ Ustawienia" - Configure entity detection
- Click extension icon → "📊 Dashboard" - Test anonymization

## Detected Entities

### Polish Specific
- **PESEL**: Personal identification number
- **NIP**: Tax identification number
- **REGON**: Business registry number
- **ID Card**: Polish ID card numbers
- **Passport**: Polish passport numbers

### General
- **PERSON**: Names and surnames
- **LOCATION**: Cities, addresses
- **EMAIL_ADDRESS**: Email addresses
- **PHONE_NUMBER**: Phone numbers
- **CREDIT_CARD**: Credit card numbers
- **IBAN_CODE**: Bank account numbers
- **IP_ADDRESS**: IP addresses
- **URL**: Web addresses
- **DATE_TIME**: Dates and times

## Architecture

```
┌─────────────┐
│   Chrome    │
│  Extension  │
└──────┬──────┘
       │ HTTP API
       │
┌──────▼──────┐
│   Backend   │
│  (Flask)    │
└──────┬──────┘
       │
┌──────▼──────┐
│  Presidio   │
│  + SpaCy    │
└─────────────┘
```

## Development

### Project Structure

```
chrome-extension/
├── manifest.json          # Extension configuration
├── background.js          # Service worker (API calls)
├── content-script.js      # Page interaction
├── popup.html/js          # Extension popup
├── options.html/js        # Configuration page
├── config.js              # Config management
└── icons/                 # Extension icons
```

### Building

No build step required - extension works directly from source.

### Testing

1. Make changes to code
2. Go to `chrome://extensions/`
3. Click reload icon on extension card
4. Test functionality

## Troubleshooting

### "Status: Offline"

- Verify backend is running: `curl http://localhost:4222/api/health`
- Check backend URL in extension options
- Check browser console for errors

### "Anonymization Failed"

- Ensure backend is accessible
- Check text contains detectable entities
- Verify entities are enabled in dashboard settings

### Permission Errors

- Extension requires `http://localhost` access
- For custom hosts, update `host_permissions` in manifest.json

## License

MIT

## Contributing

1. Fork repository
2. Create feature branch
3. Make changes
4. Test thoroughly
5. Submit pull request

## Links

- **Repository**: https://github.com/gacabartosz/presidio-local-anonymizer
- **Issues**: https://github.com/gacabartosz/presidio-local-anonymizer/issues
- **Presidio**: https://github.com/microsoft/presidio
