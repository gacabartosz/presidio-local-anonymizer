# Rozszerzenie Chrome - Przewodnik Instalacji

## Szybki Start

### 1. Wygeneruj ikony (wybierz jedną opcję)

**Opcja A - Online (najprościej):**
1. Przejdź do https://svgtopng.com/
2. Wgraj plik `chrome-extension/icons/icon.svg`
3. Pobierz PNG w rozmiarach: 16×16, 32×32, 48×48, 128×128
4. Zmień nazwy na: `icon-16.png`, `icon-32.png`, `icon-48.png`, `icon-128.png`
5. Umieść w `chrome-extension/icons/`

**Opcja B - ImageMagick (dla zaawansowanych):**
```bash
cd chrome-extension/icons
brew install imagemagick  # jeśli nie masz zainstalowanego
convert icon.svg -resize 16x16 icon-16.png
convert icon.svg -resize 32x32 icon-32.png
convert icon.svg -resize 48x48 icon-48.png
convert icon.svg -resize 128x128 icon-128.png
```

**Opcja C - Python PIL/Pillow:**
```bash
cd chrome-extension/icons
pip install pillow cairosvg
python3 << 'EOF'
from cairosvg import svg2png
from PIL import Image
import io

sizes = [16, 32, 48, 128]
for size in sizes:
    png_data = svg2png(url='icon.svg', output_width=size, output_height=size)
    img = Image.open(io.BytesIO(png_data))
    img.save(f'icon-{size}.png')
    print(f'✓ Created icon-{size}.png')
EOF
```

### 2. Uruchom Backend

```bash
cd /Users/gaca/presidio-local-anonymizer/backend
source .venv/bin/activate
python app.py
```

Backend powinien być dostępny na: http://localhost:4222

### 3. Załaduj Rozszerzenie do Chrome

1. Otwórz Chrome
2. Wejdź na `chrome://extensions/`
3. Włącz **Tryb dewelopera** (przełącznik w prawym górnym rogu)
4. Kliknij **Załaduj rozpakowane**
5. Wybierz folder: `/Users/gaca/presidio-local-anonymizer/chrome-extension`
6. Gotowe! Ikona Presidio pojawi się w pasku narzędzi

## Jak Używać

### 🖱️ Menu Kontekstowe
1. Zaznacz tekst z danymi osobowymi
2. Kliknij PPM → "Anonimizuj zaznaczony tekst"

### ⌨️ Skrót Klawiszowy
1. Zaznacz tekst
2. Naciśnij `Ctrl+Shift+A` (Mac: `Cmd+Shift+A`)

### 📊 Popup
- Kliknij ikonę rozszerzenia w pasku
- Sprawdź status serwisu
- Przejdź do Dashboard lub Ustawień

## Funkcje

✅ Anonimizacja zaznaczonego tekstu w dowolnym edytowalnym polu
✅ Wykrywanie PII: email, telefon, PESEL, NIP, karty, IBAN, itp.
✅ Wsparcie dla 28 typów danych (PL, US, UK, AU, SG)
✅ Działa offline - wszystko lokalnie
✅ Menu kontekstowe i skrót klawiszowy
✅ Popup z statusem serwisu

## Permissions Explained

```json
"permissions": ["activeTab", "storage"]
```
- `activeTab` - dostęp do aktywnej karty (do zamiany tekstu)
- `storage` - przechowywanie ustawień lokalnie

```json
"host_permissions": ["http://localhost:4222/*"]
```
- Komunikacja tylko z lokalnym backendem
- Żadne dane nie trafiają do internetu

## Rozwiązywanie Problemów

### ❌ Błąd: "Nie można załadować rozszerzenia"
→ Upewnij się, że folder `chrome-extension/icons/` zawiera wszystkie 4 pliki PNG

### ❌ "Service Offline" w popupie
→ Backend nie działa. Uruchom: `python backend/app.py`

### ❌ Tekst się nie anonimizuje
→ Sprawdź konsolę (F12) i upewnij się, że backend odpowiada

### ❌ Brak ikon
→ Wygeneruj pliki PNG zgodnie z instrukcją powyżej

## Development

Aby edytować rozszerzenie:
1. Zmień kod w `chrome-extension/`
2. Wejdź na `chrome://extensions/`
3. Kliknij ikonę odświeżania ↻ przy rozszerzeniu

## Bezpieczeństwo

- ✅ Wszystko działa lokalnie
- ✅ Żadne dane nie opuszczają Twojego komputera
- ✅ Backend tylko na localhost:4222
- ✅ Brak połączeń zewnętrznych

## Następne Kroki

1. **Publikacja w Chrome Web Store** (opcjonalnie)
   - Wymaga konta dewelopera ($5 jednorazowo)
   - Przegląd zajmuje 1-3 dni

2. **Firefox Add-on** (przyszłość)
   - Manifest v3 jest kompatybilny
   - Wymaga małych zmian

3. **Edge Extension** (przyszłość)
   - Również kompatybilny z Manifest v3

---

**Autor**: Bartosz Gaca
**Licencja**: MIT
**GitHub**: https://github.com/gacabartosz/presidio-local-anonymizer
