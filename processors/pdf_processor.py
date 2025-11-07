"""
Procesor dla dokumentów PDF z osadzonym tekstem (text layer).
Nie wymaga OCR - używa tekstu embedded w PDF.
"""

import json
import logging
from pathlib import Path
from typing import Dict, Any, Tuple, List
from datetime import datetime

try:
    import PyPDF2
    from reportlab.pdfgen import canvas
    from reportlab.lib.pagesizes import letter
    from reportlab.lib.utils import simpleSplit
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
except ImportError:
    PyPDF2 = None
    canvas = None

from app.analyzer import get_supported_entities
from app.anonymizer import anonymize_text, prepare_anonymization_report

logger = logging.getLogger("app.pdf_processor")


def process_pdf(
    file_path: Path,
    analyzer: Any,
    config: Dict[str, Any]
) -> Tuple[Path, Dict[str, Any]]:
    """
    Przetwarza dokument PDF z osadzonym tekstem (bez OCR).

    Args:
        file_path: Ścieżka do pliku PDF
        analyzer: Skonfigurowany Presidio AnalyzerEngine
        config: Konfiguracja encji

    Returns:
        tuple: (output_path, report) - ścieżka do zanonimizowanego pliku i raport JSON

    Note:
        MVP: Formatowanie PDF jest uproszczone - tekst jest renderowany jako plain text.
        Złożone layouty, obrazy, fonty mogą nie być zachowane.
    """
    if PyPDF2 is None:
        raise ImportError(
            "PyPDF2 i reportlab nie są zainstalowane. "
            "Uruchom: pip install PyPDF2 reportlab"
        )

    logger.info(f"Rozpoczynam przetwarzanie PDF: {file_path.name}")

    try:
        # Sprawdź czy PDF ma tekst
        if not _pdf_has_text(file_path):
            logger.warning(f"PDF {file_path.name} wydaje się być skanem - użyj OCR processor")
            raise ValueError(
                f"PDF {file_path.name} nie zawiera tekstu lub jest skanem. "
                "Użyj process_pdf_with_ocr() dla skanów."
            )

        # Wczytaj PDF
        with open(file_path, 'rb') as f:
            pdf_reader = PyPDF2.PdfReader(f)
            num_pages = len(pdf_reader.pages)

            logger.debug(f"PDF zawiera {num_pages} stron")

            # Wyekstrahuj i przetworz tekst ze wszystkich stron
            all_pages_anonymized = []
            all_analyzer_results = []

            for page_num in range(num_pages):
                page = pdf_reader.pages[page_num]
                page_text = page.extract_text()

                if page_text.strip():
                    logger.debug(f"Strona {page_num + 1}: {len(page_text)} znaków")

                    # Analizuj tekst strony
                    entities = get_supported_entities(config)
                    threshold = config.get('threshold', 0.35)

                    results = analyzer.analyze(
                        text=page_text,
                        entities=entities,
                        language='pl',
                        score_threshold=threshold
                    )

                    # Anonimizuj tekst
                    anonymized_text = anonymize_text(page_text, results, config)

                    all_pages_anonymized.append(anonymized_text)
                    all_analyzer_results.extend(results)

                    logger.debug(f"Strona {page_num + 1}: {len(results)} wykryć PII")
                else:
                    all_pages_anonymized.append("")

        # Utwórz nowy PDF z zanonimizowanym tekstem
        output_path = file_path.parent / f"{file_path.stem}.anon.pdf"

        _create_pdf_from_text(all_pages_anonymized, output_path)

        logger.info(f"Zapisano zanonimizowany PDF: {output_path}")

        # Przygotuj raport
        report = {
            "source_file": str(file_path),
            "output_file": str(output_path),
            "status": "success",
            "timestamp": datetime.now().isoformat(),
            "format": "PDF",
            "pages": num_pages,
            "note": "PDF text layer only - complex formatting may be simplified",
            "analysis": prepare_anonymization_report(all_analyzer_results, config)
        }

        # Zapisz raport jako osobny plik JSON
        report_path = output_path.with_suffix('.anon.json')
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)

        logger.info(f"Raport zapisany: {report_path}")

        return output_path, report

    except Exception as e:
        logger.exception(f"Błąd podczas przetwarzania {file_path.name}: {e}")
        raise


def _pdf_has_text(file_path: Path, min_chars: int = 50) -> bool:
    """
    Sprawdza czy PDF ma osadzony tekst (text layer).

    Args:
        file_path: Ścieżka do PDF
        min_chars: Minimalna liczba znaków aby uznać że PDF ma tekst

    Returns:
        bool: True jeśli PDF ma tekst, False jeśli jest skanem
    """
    try:
        with open(file_path, 'rb') as f:
            pdf_reader = PyPDF2.PdfReader(f)

            # Sprawdź kilka pierwszych stron
            pages_to_check = min(3, len(pdf_reader.pages))

            total_chars = 0
            for i in range(pages_to_check):
                text = pdf_reader.pages[i].extract_text()
                total_chars += len(text.strip())

                if total_chars > min_chars:
                    return True

            return total_chars > min_chars

    except Exception as e:
        logger.warning(f"Nie można sprawdzić czy PDF ma tekst: {e}")
        return False


def _create_pdf_from_text(pages_text: List[str], output_path: Path) -> None:
    """
    Tworzy nowy PDF z listy tekstów (jeden tekst = jedna strona).

    Args:
        pages_text: Lista tekstów dla każdej strony
        output_path: Ścieżka do zapisu PDF

    Note:
        MVP: Prosty rendering - tekst jest renderowany jako plain text,
        bez zachowania oryginalnego formatowania.
    """
    c = canvas.Canvas(str(output_path), pagesize=letter)

    width, height = letter
    margin = 50
    line_height = 14
    max_width = width - 2 * margin

    for page_text in pages_text:
        if not page_text.strip():
            c.showPage()  # Pusta strona
            continue

        y = height - margin  # Start od góry

        # Podziel tekst na linie
        lines = page_text.split('\n')

        for line in lines:
            if not line.strip():
                y -= line_height
                continue

            # Podziel długie linie
            wrapped_lines = simpleSplit(line, 'Helvetica', 10, max_width)

            for wrapped_line in wrapped_lines:
                if y < margin + line_height:
                    # Nowa strona jeśli brak miejsca
                    c.showPage()
                    y = height - margin

                c.drawString(margin, y, wrapped_line)
                y -= line_height

        c.showPage()  # Nowa strona

    c.save()
    logger.debug(f"PDF utworzony: {output_path}")
