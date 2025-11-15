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
from presidio_analyzer import RecognizerResult
from presidio_analyzer.entity_recognizer import EntityRecognizer

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

    # Dodanie rozpoznawacza SpaCy dla polskich etykiet NER
    _add_polish_spacy_recognizer(analyzer, nlp_engine)

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


def _add_polish_spacy_recognizer(analyzer: AnalyzerEngine, nlp_engine) -> None:
    """
    Dodaje niestandardowy rozpoznawacz SpaCy dla polskich etykiet NER.
    Mapuje polskie etykiety (persName, placeName) na encje Presidio (PERSON, LOCATION).

    Args:
        analyzer: AnalyzerEngine do którego dodajemy rozpoznawacz
        nlp_engine: Skonfigurowany silnik NLP SpaCy
    """

    class PolishSpacyRecognizer(EntityRecognizer):
        """Rozpoznawacz mapujący polskie etykiety SpaCy na encje Presidio"""

        POLISH_TO_PRESIDIO_MAPPING = {
            "persName": "PERSON",        # Polskie imiona i nazwiska
            "placeName": "LOCATION",      # Polskie nazwy miejscowości
            "geogName": "LOCATION",       # Nazwy geograficzne
            "orgName": "ORGANIZATION",    # Nazwy organizacji
        }

        def __init__(self):
            # Obsługiwane encje to wartości z mapowania
            supported_entities = list(set(self.POLISH_TO_PRESIDIO_MAPPING.values()))
            super().__init__(
                supported_entities=supported_entities,
                supported_language="pl",
                name="PolishSpacyRecognizer"
            )

        def load(self) -> None:
            """Załaduj model - nie wymagane dla tego rozpoznawacza"""
            pass

        def analyze(self, text: str, entities: list, nlp_artifacts=None):
            """
            Analizuj tekst używając SpaCy i mapuj polskie etykiety na encje Presidio.

            Args:
                text: Tekst do analizy
                entities: Lista encji do wykrycia
                nlp_artifacts: Wyniki SpaCy NLP

            Returns:
                Lista RecognizerResult
            """
            results = []

            if not nlp_artifacts or not hasattr(nlp_artifacts, 'entities'):
                return results

            # Iteruj przez encje wykryte przez SpaCy
            for ent in nlp_artifacts.entities:
                # Sprawdź czy etykieta SpaCy ma mapowanie na encję Presidio
                presidio_entity = self.POLISH_TO_PRESIDIO_MAPPING.get(ent.label_)

                if presidio_entity and presidio_entity in entities:
                    # Utwórz wynik rozpoznania
                    result = RecognizerResult(
                        entity_type=presidio_entity,
                        start=ent.start_char,
                        end=ent.end_char,
                        score=0.85  # Wysoki wynik pewności
                    )
                    results.append(result)

            return results

    # Dodaj rozpoznawacz do analyzera
    polish_recognizer = PolishSpacyRecognizer()
    analyzer.registry.add_recognizer(polish_recognizer)
    logger.info("Dodano rozpoznawacz polskich etykiet SpaCy (persName->PERSON, placeName->LOCATION)")


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
