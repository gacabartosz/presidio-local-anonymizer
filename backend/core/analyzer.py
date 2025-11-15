"""
Moduł analizatora PII wykorzystujący Presidio AnalyzerEngine.
Konfiguruje silnik NLP dla języka polskiego i dodaje niestandardowe rozpoznawacze.
"""

import os
import yaml
from pathlib import Path
from typing import Dict, Any
import logging

from presidio_analyzer import AnalyzerEngine, PatternRecognizer, Pattern
from presidio_analyzer.nlp_engine import SpacyNlpEngine, NlpEngineProvider

logger = logging.getLogger("app.analyzer")


def build_analyzer() -> tuple[AnalyzerEngine, Dict[str, Any]]:
    """
    Buduje i konfiguruje Presidio AnalyzerEngine z polskim modelem NLP.

    Returns:
        tuple: (analyzer, config) - skonfigurowany analyzer i wczytana konfiguracja
    """
    # Znajdź ścieżkę do pliku konfiguracyjnego
    config_path = Path(__file__).parent.parent / "config" / "entities.yaml"

    if not config_path.exists():
        raise FileNotFoundError(f"Nie znaleziono pliku konfiguracji: {config_path}")

    # Wczytaj konfigurację
    with open(config_path, 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)

    logger.info(f"Wczytano konfigurację z: {config_path}")

    # Konfiguracja modelu SpaCy dla języka polskiego
    nlp_configuration = {
        "nlp_engine_name": "spacy",
        "models": [
            {
                "lang_code": "pl",
                "model_name": "pl_core_news_md"
            }
        ]
    }

    # Inicjalizacja silnika NLP
    try:
        nlp_engine = NlpEngineProvider(nlp_configuration=nlp_configuration).create_engine()
        logger.info("Silnik NLP SpaCy zainicjalizowany dla języka polskiego")
    except Exception as e:
        logger.error(f"Błąd podczas inicjalizacji silnika NLP: {e}")
        raise RuntimeError(
            "Nie udało się zainicjalizować modelu SpaCy. "
            "Upewnij się, że model pl_core_news_md jest zainstalowany: "
            "python -m spacy download pl_core_news_md"
        ) from e

    # Utworzenie AnalyzerEngine
    analyzer = AnalyzerEngine(nlp_engine=nlp_engine, supported_languages=["pl"])

    # Dodanie niestandardowych rozpoznawaczy dla polskich encji
    _add_custom_recognizers(analyzer, config)

    logger.info(f"Analyzer gotowy. Obsługiwane encje: {list(config['entities'].keys())}")

    return analyzer, config


def _add_custom_recognizers(analyzer: AnalyzerEngine, config: Dict[str, Any]) -> None:
    """
    Dodaje niestandardowe rozpoznawacze pattern-based dla encji z konfiguracji.

    Args:
        analyzer: AnalyzerEngine do którego dodajemy rozpoznawacze
        config: Słownik konfiguracji wczytany z YAML
    """
    for entity_name, entity_config in config['entities'].items():
        patterns = entity_config.get('patterns')

        if not patterns:
            continue  # Pomiń encje bez wzorców regex

        # Przygotuj listę wzorców dla PatternRecognizer
        pattern_list = []
        for pattern in patterns:
            pattern_list.append(Pattern(
                name=pattern['name'],
                regex=pattern['regex'],
                score=pattern['score']
            ))

        # Utwórz rozpoznawacz
        recognizer = PatternRecognizer(
            supported_entity=entity_name,
            patterns=pattern_list,
            supported_language="pl"
        )

        # Dodaj do registry analyzera
        analyzer.registry.add_recognizer(recognizer)

        logger.info(f"Dodano niestandardowy rozpoznawacz dla: {entity_name} ({len(pattern_list)} wzorców)")


def get_supported_entities(config: Dict[str, Any]) -> list[str]:
    """
    Zwraca listę nazw włączonych encji z konfiguracji.

    Args:
        config: Słownik konfiguracji

    Returns:
        list: Lista nazw włączonych encji
    """
    enabled_entities = []
    for entity_name, entity_config in config['entities'].items():
        if entity_config.get('enabled', True):
            enabled_entities.append(entity_name)
    return enabled_entities
