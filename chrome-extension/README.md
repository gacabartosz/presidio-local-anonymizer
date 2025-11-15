# Presidio Browser Anonymizer - Chrome Extension

Rozszerzenie Chrome do anonimizacji danych osobowych w czasie rzeczywistym.

## Funkcje

- **Anonimizacja zaznaczonego tekstu** - Kliknij prawym przyciskiem myszy na zaznaczonym tekście → "Anonimizuj zaznaczony tekst"
- **Skrót klawiszowy** - `Ctrl+Shift+A` (Mac: `Cmd+Shift+A`) anonimizuje zaznaczony tekst
- **Popup z statusem** - Sprawdzenie statusu serwisu i szybki dostęp do Dashboard i Ustawień
- **Automatyczna detekcja PII** - Wykrywa i maskuje:
  - Adresy email
  - Numery telefonów
  - PESEL, NIP, dowód osobisty, paszport (PL)
  - Karty kredytowe, IBAN
  - Adresy IP, URL
  - Daty, lokalizacje
  - SSN, paszporty (US)
  - NHS, ABN, TFN, Medicare (UK/AU/SG)

## Wymagania

**Backend musi być uruchomiony!**

```bash
cd backend
source .venv/bin/activate
python app.py
```

Backend działa na: `http://localhost:4222`

## Instalacja Rozszerzenia

### 1. Przygotuj ikony (opcjonalne)

Rozszerzenie wymaga ikon PNG w różnych rozmiarach. Możesz:

**Opcja A: Użyj narzędzia online do konwersji SVG → PNG**
- Otwórz https://svgtopng.com/
- Wgraj plik `icons/icon.svg`
- Wygeneruj PNG w rozmiarach: 16x16, 32x32, 48x48, 128x128
- Zapisz jako `icon-16.png`, `icon-32.png`, `icon-48.png`, `icon-128.png`
- Umieść w folderze `icons/`

**Opcja B: Użyj ImageMagick (jeśli zainstalowany)**
```bash
cd chrome-extension/icons
convert icon.svg -resize 16x16 icon-16.png
convert icon.svg -resize 32x32 icon-32.png
convert icon.svg -resize 48x48 icon-48.png
convert icon.svg -resize 128x128 icon-128.png
```

**Opcja C: Użyj tymczasowych ikon (dla testów)**
Możesz tymczasowo użyć dowolnych obrazów PNG o odpowiednich rozmiarach, aby przetestować rozszerzenie.

### 2. Załaduj rozszerzenie do Chrome

1. Otwórz Chrome i przejdź do: `chrome://extensions/`
2. Włącz **Tryb dewelopera** (przełącznik w prawym górnym rogu)
3. Kliknij **Załaduj rozpakowane**
4. Wybierz folder: `/Users/gaca/presidio-local-anonymizer/chrome-extension`

### 3. Gotowe!

Rozszerzenie jest zainstalowane. Zobaczysz ikonę Presidio w pasku narzędzi Chrome.

## Użycie

### Metoda 1: Menu kontekstowe
1. Zaznacz tekst z danymi osobowymi na dowolnej stronie
2. Kliknij prawym przyciskiem myszy
3. Wybierz **"Anonimizuj zaznaczony tekst"**
4. Tekst zostanie zastąpiony wersją zanonimizowaną

### Metoda 2: Skrót klawiszowy
1. Zaznacz tekst z danymi osobowymi
2. Naciśnij `Ctrl+Shift+A` (Windows/Linux) lub `Cmd+Shift+A` (Mac)
3. Tekst zostanie automatycznie zanonimizowany

### Metoda 3: Popup
1. Kliknij ikonę rozszerzenia w pasku narzędzi
2. Sprawdź status serwisu
3. Kliknij **Dashboard** lub **Ustawienia** aby otworzyć interfejs webowy

## Rozwiązywanie problemów

### "Status Serwisu: Offline"
- Upewnij się, że backend jest uruchomiony: `python backend/app.py`
- Sprawdź czy backend działa: http://localhost:4222/api/health

### Rozszerzenie nie anonimizuje tekstu
- Sprawdź konsolę Chrome (F12 → Console) dla błędów
- Upewnij się, że backend odpowiada poprawnie
- Spróbuj przeładować rozszerzenie w `chrome://extensions/`

### Ikony nie wyświetlają się
- Upewnij się, że wygenerowałeś pliki PNG w folderze `icons/`
- Przeładuj rozszerzenie w `chrome://extensions/`

## Bezpieczeństwo

- Rozszerzenie komunikuje się **TYLKO** z localhost:4222
- Żadne dane nie są wysyłane do internetu
- Backend działa lokalnie na Twoim komputerze
- Wszystkie dane pozostają w Twojej sieci lokalnej

## Wsparcie

- **GitHub**: https://github.com/gacabartosz/presidio-local-anonymizer
- **Backend API**: http://localhost:4222/api
- **Dashboard**: http://localhost:4222/dashboard
- **Ustawienia**: http://localhost:4222/

## Licencja

MIT License - Zobacz plik LICENSE w głównym katalogu projektu.
