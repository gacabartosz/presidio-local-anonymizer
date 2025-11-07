"""
Procesor dla dokumentów ODT (LibreOffice/OpenOffice).
Anonimizuje tekst poprzez ekstrakcję, przetworzenie i utworzenie nowego dokumentu.
"""

import json
import logging
from pathlib import Path
from typing import Dict, Any, Tuple
from datetime import datetime

from odf import text, teletype
from odf.opendocument import load, OpenDocumentText
from presidio_analyzer import AnalyzerEngine

from app.analyzer import get_supported_entities
from app.anonymizer import anonymize_text, prepare_anonymization_report

logger = logging.getLogger("app.odt_processor")


def process_odt(
    file_path: Path,
    analyzer: AnalyzerEngine,
    config: Dict[str, Any]
) -> Tuple[Path, Dict[str, Any]]:
    """
    Przetwarza dokument ODT, anonimizując zawartość.

    Args:
        file_path: Ścieżka do pliku ODT
        analyzer: Skonfigurowany Presidio AnalyzerEngine
        config: Konfiguracja encji

    Returns:
        tuple: (output_path, report) - ścieżka do zanonimizowanego pliku i raport JSON

    Note:
        MVP: Uproszczona wersja - ekstrakcja całego tekstu, anonimizacja i zapisanie
        jako prosty dokument. Złożona struktura i formatowanie nie są zachowane.
    """
    logger.info(f"Rozpoczynam przetwarzanie ODT: {file_path.name}")

    try:
        # Wczytaj dokument
        doc = load(file_path)

        # Wyekstrahuj cały tekst z dokumentu (linearyzacja)
        extracted_text = _extract_all_text(doc)
        logger.debug(f"Wyekstrahowano {len(extracted_text)} znaków tekstu")

        if not extracted_text.strip():
            logger.warning("Dokument nie zawiera tekstu")
            # Utwórz pusty dokument wyjściowy
            output_doc = OpenDocumentText()
        else:
            # Przeanalizuj tekst
            entities = get_supported_entities(config)
            threshold = config.get('threshold', 0.35)

            analyzer_results = analyzer.analyze(
                text=extracted_text,
                entities=entities,
                language='pl',
                score_threshold=threshold
            )

            logger.info(f"Wykryto {len(analyzer_results)} encji PII")

            # Anonimizuj tekst
            anonymized_text = anonymize_text(extracted_text, analyzer_results, config)

            # Utwórz nowy dokument ODT z zanonimizowanym tekstem
            output_doc = OpenDocumentText()

            # Dodaj tekst jako paragrafy (każda linia jako oddzielny paragraf)
            for line in anonymized_text.split('\n'):
                p = text.P(text=line)
                output_doc.text.addElement(p)

        # Przygotuj ścieżkę wyjściową
        output_path = file_path.parent / f"{file_path.stem}.anon{file_path.suffix}"

        # Zapisz zanonimizowany dokument
        output_doc.save(output_path)
        logger.info(f"Zapisano zanonimizowany dokument: {output_path}")

        # Przygotuj raport
        if extracted_text.strip():
            analysis_report = prepare_anonymization_report(analyzer_results, config)
        else:
            analysis_report = {"total_detections": 0, "entities": {}}

        report = {
            "source_file": str(file_path),
            "output_file": str(output_path),
            "status": "success",
            "timestamp": datetime.now().isoformat(),
            "format": "ODT",
            "note": "MVP: Uproszczone formatowanie - struktura dokumentu została linearyzowana",
            "analysis": analysis_report
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


def _extract_all_text(doc: OpenDocumentText) -> str:
    """
    Ekstrahuje cały tekst z dokumentu ODT.

    Args:
        doc: Obiekt dokumentu ODT (OpenDocumentText)

    Returns:
        str: Wyekstrahowany tekst (linearyzowany)
    """
    text_content = []

    # Iteruj przez wszystkie elementy tekstowe
    for element in doc.getElementsByType(text.P):  # Paragrafy
        para_text = teletype.extractText(element)
        if para_text.strip():
            text_content.append(para_text)

    for element in doc.getElementsByType(text.H):  # Nagłówki
        heading_text = teletype.extractText(element)
        if heading_text.strip():
            text_content.append(heading_text)

    # Połącz wszystkie teksty
    full_text = '\n'.join(text_content)

    return full_text
