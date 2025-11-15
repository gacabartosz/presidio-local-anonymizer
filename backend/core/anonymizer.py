"""
Moduł anonimizacji PII wykorzystujący Presidio AnonymizerEngine.
Zastępuje wykryte encje odpowiednimi maskami zgodnie z konfiguracją.
"""

import logging
from typing import Dict, Any, List

from presidio_analyzer import RecognizerResult
from presidio_anonymizer import AnonymizerEngine
from presidio_anonymizer.entities import OperatorConfig

logger = logging.getLogger("app.anonymizer")


def anonymize_text(
    text: str,
    analyzer_results: List[RecognizerResult],
    config: Dict[str, Any]
) -> str:
    """
    Anonimizuje tekst zastępując wykryte encje odpowiednimi maskami.

    Args:
        text: Tekst do zanonimizowania
        analyzer_results: Lista wyników z Presidio Analyzer
        config: Słownik konfiguracji z maskami dla encji

    Returns:
        str: Zanonimizowany tekst

    Example:
        >>> text = "Jan Kowalski, email: jan@example.com"
        >>> results = analyzer.analyze(text, ...)
        >>> anonymized = anonymize_text(text, results, config)
        >>> print(anonymized)
        [OSOBA], email: [EMAIL]
    """
    if not analyzer_results:
        logger.debug("Brak wykrytych encji do zanonimizowania")
        return text

    # Utwórz engine anonimizacji
    anonymizer = AnonymizerEngine()

    # Przygotuj mapowanie encji na operatory (maski)
    operators = {}
    for entity_name, entity_config in config['entities'].items():
        mask = entity_config.get('mask', f"[{entity_name}]")
        operators[entity_name] = OperatorConfig("replace", {"new_value": mask})

    # Loguj informacje o wykrytych encjach (bez wartości PII!)
    entity_counts = {}
    for result in analyzer_results:
        entity_counts[result.entity_type] = entity_counts.get(result.entity_type, 0) + 1

    logger.info(f"Wykryto encje: {entity_counts}")

    # Wykonaj anonimizację
    anonymized_result = anonymizer.anonymize(
        text=text,
        analyzer_results=analyzer_results,
        operators=operators
    )

    logger.debug(f"Anonimizacja zakończona. Długość tekstu: {len(text)} -> {len(anonymized_result.text)}")

    return anonymized_result.text


def prepare_anonymization_report(
    analyzer_results: List[RecognizerResult],
    config: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Przygotowuje raport z analizy wykrytych encji (bez wartości PII).

    Args:
        analyzer_results: Lista wyników z Presidio Analyzer
        config: Słownik konfiguracji

    Returns:
        dict: Raport zawierający statystyki wykrytych encji
    """
    if not analyzer_results:
        return {"total_detections": 0, "entities": {}}

    # Zlicz wykrycia według typów
    entity_stats = {}
    for result in analyzer_results:
        entity_type = result.entity_type

        if entity_type not in entity_stats:
            entity_stats[entity_type] = {
                "count": 0,
                "mask": config['entities'].get(entity_type, {}).get('mask', f"[{entity_type}]"),
                "avg_score": 0.0,
                "scores": []
            }

        entity_stats[entity_type]["count"] += 1
        entity_stats[entity_type]["scores"].append(result.score)

    # Oblicz średnie score
    for entity_type in entity_stats:
        scores = entity_stats[entity_type]["scores"]
        entity_stats[entity_type]["avg_score"] = sum(scores) / len(scores)
        del entity_stats[entity_type]["scores"]  # Usuń szczegółowe score z raportu

    total_detections = sum(stats["count"] for stats in entity_stats.values())

    report = {
        "total_detections": total_detections,
        "entities": entity_stats,
        "threshold_used": config.get('threshold', 0.35)
    }

    logger.info(f"Wygenerowano raport: {total_detections} wykrytych encji")

    return report
