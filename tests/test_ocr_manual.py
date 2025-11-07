#!/usr/bin/env python3
"""
Test ręczny OCR - tworzy testowy obraz i przetwarza przez OCR.
Użycie: python tests/test_ocr_manual.py
"""

import sys
from pathlib import Path

# Dodaj katalog główny do PATH
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    from PIL import Image, ImageDraw, ImageFont
    import pytesseract
except ImportError:
    print("❌ Błąd: Brak wymaganych bibliotek!")
    print("Zainstaluj: pip install pillow pytesseract")
    sys.exit(1)


def create_test_image(output_path: Path):
    """Tworzy testowy obraz z danymi osobowymi."""
    print(f"📝 Tworzenie testowego obrazu: {output_path}")

    # Utwórz obraz
    img = Image.new('RGB', (800, 500), color='white')
    draw = ImageDraw.Draw(img)

    # Użyj domyślnej czcionki lub systemowej
    try:
        # Spróbuj załadować czcionkę systemową (macOS)
        font = ImageFont.truetype('/System/Library/Fonts/Helvetica.ttc', 30)
    except:
        try:
            # Fallback dla innych systemów
            font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 30)
        except:
            # Ostatni fallback - domyślna czcionka
            font = ImageFont.load_default()
            print("⚠️  Używam domyślnej czcionki (może być mała)")

    # Dodaj nagłówek
    draw.text((50, 20), 'DANE TESTOWE - DO ANONIMIZACJI', fill='red', font=font)

    # Dodaj testowe dane osobowe
    y = 80
    test_data = [
        'Imię i nazwisko: Jan Kowalski',
        'Email: jan.kowalski@example.com',
        'Telefon: +48 123 456 789',
        'PESEL: 92010212345',
        'NIP: 1234567890',
        'Adres: ul. Testowa 123, Warszawa'
    ]

    for text in test_data:
        draw.text((50, y), text, fill='black', font=font)
        y += 60

    # Zapisz obraz
    img.save(output_path)
    print(f"✅ Obraz utworzony: {output_path}")
    print(f"   Wielkość: {output_path.stat().st_size / 1024:.1f} KB")


def test_ocr_detection(image_path: Path):
    """Testuje czy Tesseract wykrywa tekst."""
    print(f"\n🔍 Test OCR na obrazie: {image_path}")

    try:
        # Otwórz obraz
        img = Image.open(image_path)

        # Test 1: Czy Tesseract działa
        print("\n1️⃣ Sprawdzanie wersji Tesseract...")
        try:
            version = pytesseract.get_tesseract_version()
            print(f"   ✅ Tesseract version: {version}")
        except:
            print("   ❌ Tesseract nie jest zainstalowany!")
            print("   Instalacja: brew install tesseract tesseract-lang")
            return False

        # Test 2: Czy polski model jest dostępny
        print("\n2️⃣ Sprawdzanie polskiego modelu językowego...")
        try:
            langs = pytesseract.get_languages()
            if 'pol' in langs:
                print(f"   ✅ Polski model (pol) jest dostępny")
                print(f"   Dostępne języki: {', '.join(langs[:10])}...")
            else:
                print(f"   ⚠️  Polski model NIE jest dostępny!")
                print(f"   Instalacja: brew install tesseract-lang")
        except:
            print("   ⚠️  Nie można sprawdzić języków")

        # Test 3: Ekstrakcja tekstu (angielski)
        print("\n3️⃣ Test OCR (język angielski)...")
        text_eng = pytesseract.image_to_string(img, lang='eng')
        print(f"   Wykryto {len(text_eng)} znaków")
        if text_eng.strip():
            print(f"   ✅ OCR działa!")
            print(f"   Pierwsze 100 znaków: {text_eng[:100].strip()}")
        else:
            print(f"   ❌ Nie wykryto tekstu!")

        # Test 4: Ekstrakcja tekstu (polski)
        print("\n4️⃣ Test OCR (język polski)...")
        try:
            text_pol = pytesseract.image_to_string(img, lang='pol')
            print(f"   Wykryto {len(text_pol)} znaków")
            if text_pol.strip():
                print(f"   ✅ OCR działa z polskim modelem!")
                print(f"   Pierwsze 100 znaków: {text_pol[:100].strip()}")
        except Exception as e:
            print(f"   ❌ Błąd z polskim modelem: {e}")
            print(f"   Instalacja: brew install tesseract-lang")

        # Test 5: Detekcja danych osobowych
        print("\n5️⃣ Sprawdzanie wykrytych danych osobowych...")
        text = text_eng if text_eng else text_pol

        checks = {
            'Jan Kowalski': 'PERSON' in text or 'Kowalski' in text,
            'Email': 'kowalski@example.com' in text or '@' in text,
            'Telefon': '+48' in text or '123' in text,
            'PESEL': '92010212345' in text or '920102' in text,
            'NIP': '1234567890' in text or '123456' in text
        }

        for item, found in checks.items():
            status = "✅" if found else "❌"
            print(f"   {status} {item}: {'wykryto' if found else 'NIE wykryto'}")

        return True

    except Exception as e:
        print(f"❌ Błąd podczas testu: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    print("=" * 70)
    print("🧪 TEST OCR - PRESIDIO LOCAL ANONYMIZER")
    print("=" * 70)

    # Ścieżka do testowego obrazu
    desktop = Path.home() / "Desktop"
    test_image = desktop / "test_ocr_presidio.png"

    # Krok 1: Utwórz testowy obraz
    create_test_image(test_image)

    # Krok 2: Testuj OCR
    success = test_ocr_detection(test_image)

    # Podsumowanie
    print("\n" + "=" * 70)
    if success:
        print("✅ TEST ZAKOŃCZONY POMYŚLNIE!")
        print(f"\n📄 Testowy obraz: {test_image}")
        print("\n💡 Następne kroki:")
        print("   1. Otwórz obraz i sprawdź czy tekst jest czytelny")
        print("   2. Przetestuj przez pełny pipeline anonimizacji:")
        print(f"      anonymize {test_image}")
        print("   3. Sprawdź wynik: test_ocr_presidio.anon.png")
    else:
        print("❌ TEST NIEUDANY - sprawdź błędy powyżej")
    print("=" * 70)


if __name__ == "__main__":
    main()
