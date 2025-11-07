"""
Procesor OCR dla skanów PDF i obrazów wykorzystujący Tesseract.
Wykrywa tekst na obrazach i zamazuje PII czarnymi prostokątami.
"""

import json
import logging
from pathlib import Path
from typing import Dict, Any, Tuple, List
from datetime import datetime

try:
    import pytesseract
    from PIL import Image, ImageDraw
    from pdf2image import convert_from_path
    import img2pdf
except ImportError:
    pytesseract = None
    Image = None
    convert_from_path = None
    img2pdf = None

from app.analyzer import get_supported_entities
from app.anonymizer import prepare_anonymization_report

logger = logging.getLogger("app.ocr_processor")


def process_pdf_with_ocr(
    file_path: Path,
    analyzer: Any,
    config: Dict[str, Any]
) -> Tuple[Path, Dict[str, Any]]:
    """
    Przetwarza skan PDF używając OCR (Tesseract).
    Zamazuje wykryte PII czarnymi prostokątami na obrazie.

    Args:
        file_path: Ścieżka do pliku PDF (skan)
        analyzer: Skonfigurowany Presidio AnalyzerEngine
        config: Konfiguracja encji

    Returns:
        tuple: (output_path, report) - ścieżka do zanonimizowanego pliku i raport JSON
    """
    if pytesseract is None or convert_from_path is None:
        raise ImportError(
            "Biblioteki OCR nie są zainstalowane. "
            "Uruchom: pip install pytesseract pdf2image pillow img2pdf\n"
            "Zainstaluj także Tesseract OCR: https://github.com/tesseract-ocr/tesseract"
        )

    logger.info(f"Rozpoczynam przetwarzanie PDF z OCR: {file_path.name}")

    try:
        # 1. Konwertuj PDF do obrazów (300 DPI dla dobrej jakości OCR)
        logger.debug("Konwersja PDF do obrazów...")
        images = convert_from_path(file_path, dpi=300)
        logger.debug(f"PDF skonwertowany do {len(images)} obrazów")

        anonymized_images = []
        all_analyzer_results = []

        # 2. Przetwórz każdą stronę
        for page_num, image in enumerate(images):
            logger.debug(f"Przetwarzanie strony {page_num + 1}/{len(images)}")

            # 3. OCR - wyekstrahuj tekst wraz z pozycjami słów
            ocr_data = pytesseract.image_to_data(
                image,
                lang='pol',  # Polski język (wymaga pliku pol.traineddata)
                output_type=pytesseract.Output.DICT
            )

            # Połącz tekst w całość
            full_text = ' '.join([
                text for text in ocr_data['text'] if text.strip()
            ])

            logger.debug(f"OCR wykrył {len(full_text)} znaków tekstu")

            # 4. Wykryj PII w tekście
            entities = get_supported_entities(config)
            threshold = config.get('threshold', 0.35)

            results = analyzer.analyze(
                text=full_text,
                entities=entities,
                language='pl',
                score_threshold=threshold
            )

            all_analyzer_results.extend(results)
            logger.debug(f"Strona {page_num + 1}: wykryto {len(results)} encji PII")

            # 5. Zamazuj PII na obrazie
            image_anonymized = _redact_image(image, ocr_data, results, full_text)
            anonymized_images.append(image_anonymized)

        # 6. Zapisz obrazy jako nowy PDF
        output_path = file_path.parent / f"{file_path.stem}.anon.pdf"

        logger.debug("Konwersja obrazów z powrotem do PDF...")
        _images_to_pdf(anonymized_images, output_path)

        logger.info(f"Zapisano zanonimizowany PDF: {output_path}")

        # Przygotuj raport
        report = {
            "source_file": str(file_path),
            "output_file": str(output_path),
            "status": "success",
            "timestamp": datetime.now().isoformat(),
            "format": "PDF_OCR",
            "pages": len(images),
            "ocr_engine": "Tesseract OCR",
            "note": "PDF scan processed with OCR - text extracted from images and redacted",
            "analysis": prepare_anonymization_report(all_analyzer_results, config)
        }

        # Zapisz raport
        report_path = output_path.with_suffix('.anon.json')
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)

        logger.info(f"Raport zapisany: {report_path}")

        return output_path, report

    except Exception as e:
        logger.exception(f"Błąd OCR dla {file_path.name}: {e}")
        raise


def process_image_with_ocr(
    file_path: Path,
    analyzer: Any,
    config: Dict[str, Any]
) -> Tuple[Path, Dict[str, Any]]:
    """
    Przetwarza obraz (PNG, JPG, TIFF) używając OCR.
    Zamazuje wykryte PII czarnymi prostokątami.

    Args:
        file_path: Ścieżka do pliku obrazu
        analyzer: Skonfigurowany Presidio AnalyzerEngine
        config: Konfiguracja encji

    Returns:
        tuple: (output_path, report)
    """
    if pytesseract is None or Image is None:
        raise ImportError(
            "Biblioteki OCR nie są zainstalowane. "
            "Uruchom: pip install pytesseract pillow"
        )

    logger.info(f"Rozpoczynam przetwarzanie obrazu z OCR: {file_path.name}")

    try:
        # Wczytaj obraz
        image = Image.open(file_path)

        # OCR
        ocr_data = pytesseract.image_to_data(
            image,
            lang='pol',
            output_type=pytesseract.Output.DICT
        )

        full_text = ' '.join([
            text for text in ocr_data['text'] if text.strip()
        ])

        logger.debug(f"OCR wykrył {len(full_text)} znaków tekstu")

        # Wykryj PII
        entities = get_supported_entities(config)
        threshold = config.get('threshold', 0.35)

        results = analyzer.analyze(
            text=full_text,
            entities=entities,
            language='pl',
            score_threshold=threshold
        )

        logger.debug(f"Wykryto {len(results)} encji PII")

        # Zamazuj
        image_anonymized = _redact_image(image, ocr_data, results, full_text)

        # Zapisz
        output_path = file_path.parent / f"{file_path.stem}.anon{file_path.suffix}"
        image_anonymized.save(output_path)

        logger.info(f"Zapisano zanonimizowany obraz: {output_path}")

        # Raport
        report = {
            "source_file": str(file_path),
            "output_file": str(output_path),
            "status": "success",
            "timestamp": datetime.now().isoformat(),
            "format": f"IMAGE_{file_path.suffix.upper()[1:]}",
            "ocr_engine": "Tesseract OCR",
            "note": "Image processed with OCR - text extracted and redacted",
            "analysis": prepare_anonymization_report(results, config)
        }

        report_path = output_path.with_suffix('.anon.json')
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)

        logger.info(f"Raport zapisany: {report_path}")

        return output_path, report

    except Exception as e:
        logger.exception(f"Błąd OCR dla obrazu {file_path.name}: {e}")
        raise


def _redact_image(
    image: Any,
    ocr_data: dict,
    pii_results: List,
    full_text: str
) -> Any:
    """
    Zamazuje PII na obrazie czarnymi prostokątami.

    Args:
        image: Obraz PIL
        ocr_data: Dane z Tesseract (pozycje słów)
        pii_results: Wykryte PII z Presidio
        full_text: Pełny tekst z OCR

    Returns:
        Zanonimizowany obraz
    """
    # Utwórz kopię obrazu
    img_copy = image.copy()
    draw = ImageDraw.Draw(img_copy)

    # Dla każdego wykrytego PII znajdź pozycję na obrazie
    for result in pii_results:
        start = result.start
        end = result.end
        pii_text = full_text[start:end]

        logger.debug(f"Szukam bounding box dla: '{pii_text}'")

        # Znajdź pozycje słów w OCR
        boxes = _find_word_boxes(pii_text, ocr_data, full_text)

        # Zamazuj każdy box
        for box in boxes:
            x, y, w, h = box
            # Rysuj czarny prostokąt (z małym marginesem)
            padding = 2
            draw.rectangle(
                [x - padding, y - padding, x + w + padding, y + h + padding],
                fill='black'
            )
            logger.debug(f"Zamazano obszar: ({x}, {y}, {w}, {h})")

    return img_copy


def _find_word_boxes(
    pii_text: str,
    ocr_data: dict,
    full_text: str
) -> List[Tuple[int, int, int, int]]:
    """
    Znajduje bounding boxy dla słów PII na obrazie.

    Args:
        pii_text: Tekst PII do znalezienia
        ocr_data: Dane z Tesseract
        full_text: Pełny tekst z OCR

    Returns:
        List[(x, y, width, height)] - lista prostokątów
    """
    boxes = []

    # Tokenizuj PII (rozbij na słowa)
    pii_words = pii_text.split()

    # Buduj pełny tekst z OCR wraz z indeksami
    ocr_text_with_indices = []
    current_pos = 0

    for i, word in enumerate(ocr_data['text']):
        if word.strip():
            ocr_text_with_indices.append({
                'word': word,
                'index': i,
                'start': current_pos,
                'end': current_pos + len(word)
            })
            current_pos += len(word) + 1  # +1 dla spacji

    # Znajdź pozycje słów PII w OCR
    for pii_word in pii_words:
        # Szukaj słowa w OCR (case-insensitive)
        for ocr_item in ocr_text_with_indices:
            if pii_word.lower() in ocr_item['word'].lower():
                idx = ocr_item['index']

                x = ocr_data['left'][idx]
                y = ocr_data['top'][idx]
                w = ocr_data['width'][idx]
                h = ocr_data['height'][idx]

                if w > 0 and h > 0:  # Sprawdź czy box jest poprawny
                    boxes.append((x, y, w, h))
                    logger.debug(f"Znaleziono box dla '{pii_word}': ({x}, {y}, {w}, {h})")
                    break

    return boxes


def _images_to_pdf(images: List, output_path: Path) -> None:
    """
    Konwertuje listę obrazów PIL do jednego pliku PDF.

    Args:
        images: Lista obrazów PIL
        output_path: Ścieżka do zapisu PDF
    """
    # Zapisz obrazy tymczasowo
    import tempfile
    temp_dir = Path(tempfile.mkdtemp())

    image_paths = []
    for i, img in enumerate(images):
        # Konwertuj do RGB jeśli RGBA
        if img.mode == 'RGBA':
            img = img.convert('RGB')

        temp_path = temp_dir / f"page_{i:04d}.png"
        img.save(temp_path, 'PNG')
        image_paths.append(str(temp_path))

    # Konwertuj do PDF
    with open(output_path, 'wb') as f:
        f.write(img2pdf.convert(image_paths))

    # Wyczyść pliki tymczasowe
    for img_path in image_paths:
        Path(img_path).unlink()
    temp_dir.rmdir()

    logger.debug(f"Zapisano PDF z {len(images)} stron")
