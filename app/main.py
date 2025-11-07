"""
Główny moduł aplikacji - CLI do anonimizacji dokumentów.
Obsługuje pliki DOCX, ODT, PDF i obrazy (PNG, JPG, TIFF) z OCR, pojedyncze pliki lub całe foldery.
"""

import argparse
import json
import logging
import logging.config
import sys
import yaml
from pathlib import Path
from typing import Dict, Any, List, Optional

from app.analyzer import build_analyzer
from processors.docx_processor import process_docx
from processors.odt_processor import process_odt
from processors.pdf_processor import process_pdf
from processors.ocr_processor import process_pdf_with_ocr, process_image_with_ocr

# Konfiguracja logowania
logging_config_path = Path(__file__).parent.parent / "config" / "logging.yaml"
if logging_config_path.exists():
    with open(logging_config_path, 'r') as f:
        log_config = yaml.safe_load(f)
        logging.config.dictConfig(log_config)

logger = logging.getLogger("app.main")


def main():
    """
    Główna funkcja aplikacji CLI.
    """
    parser = argparse.ArgumentParser(
        description="System anonimizacji dokumentów wykorzystujący Microsoft Presidio",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Przykłady użycia:
  %(prog)s dokument.docx
  %(prog)s folder_z_dokumentami/
  %(prog)s dokument.pdf --report szczegolowy_raport.json
  %(prog)s skan.png  (wymaga OCR - Tesseract)

Obsługiwane formaty: DOCX, ODT, PDF, PNG, JPG, TIFF (obrazy z OCR)
Wykrywane typy danych: PERSON, EMAIL, PHONE_NUMBER, PL_PESEL, PL_NIP, i więcej
        """
    )

    parser.add_argument(
        'path',
        type=str,
        help='Ścieżka do pliku lub folderu do zanonimizowania'
    )

    parser.add_argument(
        '--report',
        type=str,
        default=None,
        help='Ścieżka do pliku z raportem zbiorczym (opcjonalne)'
    )

    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Włącz szczegółowe logowanie (DEBUG)'
    )

    args = parser.parse_args()

    # Konfiguracja poziomu logowania
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
        logger.setLevel(logging.DEBUG)

    try:
        logger.info("=" * 60)
        logger.info("Uruchamianie systemu anonimizacji dokumentów")
        logger.info("=" * 60)

        # Buduj analyzer i wczytaj konfigurację
        logger.info("Inicjalizacja Presidio Analyzer...")
        analyzer, config = build_analyzer()

        # Przetwórz ścieżkę (plik lub folder)
        path = Path(args.path)

        if not path.exists():
            logger.error(f"Ścieżka nie istnieje: {path}")
            print(f"BŁĄD: Nie znaleziono: {path}", file=sys.stderr)
            return 1

        logger.info(f"Przetwarzanie: {path}")
        reports = anonymize_path(path, analyzer, config)

        if not reports:
            logger.warning("Nie znaleziono plików do przetworzenia")
            print("UWAGA: Nie znaleziono plików DOCX/ODT do przetworzenia", file=sys.stderr)
            return 0

        # Podsumowanie
        logger.info("=" * 60)
        logger.info(f"Zakończono! Przetworzono {len(reports)} plików")
        logger.info("=" * 60)

        for report in reports:
            print(f"✓ {report['source_file']} -> {report['output_file']}")

        # Zapisz raport zbiorczy jeśli podano ścieżkę
        if args.report:
            save_summary_report(reports, args.report)
            logger.info(f"Raport zbiorczy zapisano do: {args.report}")
            print(f"\nRaport zbiorczy: {args.report}")

        return 0

    except Exception as e:
        logger.exception(f"Wystąpił błąd: {e}")
        print(f"BŁĄD: {e}", file=sys.stderr)
        return 1


def anonymize_path(
    path: Path,
    analyzer: Any,
    config: Dict[str, Any]
) -> List[Dict[str, Any]]:
    """
    Przetwarza ścieżkę (plik lub folder) i zwraca listę raportów.

    Args:
        path: Ścieżka do pliku lub folderu
        analyzer: Skonfigurowany Presidio AnalyzerEngine
        config: Konfiguracja encji

    Returns:
        list: Lista raportów z każdego przetworzonego pliku
    """
    reports = []

    if path.is_file():
        # Przetwórz pojedynczy plik
        report = _process_file(path, analyzer, config)
        if report:
            reports.append(report)

    elif path.is_dir():
        # Przetwórz wszystkie obsługiwane pliki w folderze (rekurencyjnie)
        logger.info(f"Skanowanie folderu: {path}")

        # Znajdź wszystkie obsługiwane pliki
        docx_files = list(path.rglob("*.docx"))
        odt_files = list(path.rglob("*.odt"))
        pdf_files = list(path.rglob("*.pdf"))
        image_files = (
            list(path.rglob("*.png")) +
            list(path.rglob("*.jpg")) +
            list(path.rglob("*.jpeg")) +
            list(path.rglob("*.tiff")) +
            list(path.rglob("*.tif"))
        )

        all_files = docx_files + odt_files + pdf_files + image_files
        logger.info(
            f"Znaleziono {len(all_files)} plików do przetworzenia "
            f"({len(docx_files)} DOCX, {len(odt_files)} ODT, "
            f"{len(pdf_files)} PDF, {len(image_files)} obrazów)"
        )

        for file_path in all_files:
            try:
                report = _process_file(file_path, analyzer, config)
                if report:
                    reports.append(report)
            except Exception as e:
                logger.error(f"Błąd podczas przetwarzania {file_path}: {e}")
                # Kontynuuj przetwarzanie pozostałych plików

    return reports


def _process_file(
    file_path: Path,
    analyzer: Any,
    config: Dict[str, Any]
) -> Optional[Dict[str, Any]]:
    """
    Przetwarza pojedynczy plik (wybiera odpowiedni procesor).

    Args:
        file_path: Ścieżka do pliku
        analyzer: Skonfigurowany Presidio AnalyzerEngine
        config: Konfiguracja encji

    Returns:
        dict: Raport z przetwarzania lub None jeśli format nieobsługiwany
    """
    suffix = file_path.suffix.lower()

    logger.info(f"Przetwarzanie pliku: {file_path.name}")

    try:
        if suffix == '.docx':
            output_file, report = process_docx(file_path, analyzer, config)
            return report

        elif suffix == '.odt':
            output_file, report = process_odt(file_path, analyzer, config)
            return report

        elif suffix == '.pdf':
            # Automatycznie wykryj czy PDF ma tekst czy jest skanem
            from processors.pdf_processor import _pdf_has_text

            if _pdf_has_text(file_path):
                logger.info("PDF zawiera tekst - używam standardowego procesora")
                output_file, report = process_pdf(file_path, analyzer, config)
            else:
                logger.info("PDF jest skanem - używam OCR procesora")
                output_file, report = process_pdf_with_ocr(file_path, analyzer, config)

            return report

        elif suffix in ['.png', '.jpg', '.jpeg', '.tiff', '.tif']:
            logger.info("Obraz - używam OCR procesora")
            output_file, report = process_image_with_ocr(file_path, analyzer, config)
            return report

        else:
            logger.warning(f"Nieobsługiwany format pliku: {suffix}")
            return None

    except ImportError as e:
        logger.error(f"Brak wymaganych bibliotek dla {suffix}: {e}")
        print(f"BŁĄD: {e}", file=sys.stderr)
        return None


def save_summary_report(reports: List[Dict[str, Any]], output_path: str) -> None:
    """
    Zapisuje zbiorczy raport w formacie JSONL.

    Args:
        reports: Lista raportów z poszczególnych plików
        output_path: Ścieżka do pliku wyjściowego
    """
    with open(output_path, 'w', encoding='utf-8') as f:
        for report in reports:
            json.dump(report, f, ensure_ascii=False)
            f.write('\n')

    logger.info(f"Zapisano raport zbiorczy: {output_path}")


if __name__ == "__main__":
    sys.exit(main())
