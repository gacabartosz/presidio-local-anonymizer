# Dokumentacja techniczna

## Architektura systemu

### Przegląd

System składa się z następujących komponentów:

```
┌─────────────────────────────────────────────────────┐
│                    USER INPUT                       │
│  (CLI, Menu kontekstowe, Batch script)             │
└────────────────────┬────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────┐
│              app/main.py (Entry Point)              │
│  - Parsowanie argumentów                            │
│  - Koordynacja procesu                              │
│  - Obsługa błędów                                   │
└────────────────────┬────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────┐
│         app/analyzer.py (Presidio Analyzer)         │
│  - Inicjalizacja SpaCy NLP Engine                   │
│  - Konfiguracja custom recognizers                  │
│  - Analiza tekstu → RecognizerResults               │
└────────────────────┬────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────┐
│      app/anonymizer.py (Presidio Anonymizer)        │
│  - Mapowanie encji → maski                          │
│  - Zastępowanie PII w tekście                       │
│  - Generowanie raportów                             │
└────────────────────┬────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────┐
│         processors/*.py (Document Handlers)         │
│  - docx_processor.py → DOCX files                   │
│  - odt_processor.py → ODT files                     │
│  - Ekstrakcja tekstu                                │
│  - Przetwarzanie struktur (tabele, paragrafy)      │
│  - Zapisanie zanonimizowanego dokumentu             │
└─────────────────────────────────────────────────────┘
```

### Przepływ danych

1. **Input:** Użytkownik wskazuje plik lub folder
2. **Parsing:** `main.py` parsuje ścieżkę i wybiera odpowiedni procesor
3. **Loading:** Procesor wczytuje dokument (python-docx lub odfpy)
4. **Extraction:** Tekst jest ekstrahowany z paragrafów, tabel, itd.
5. **Analysis:** Presidio Analyzer wykrywa encje PII w tekście
6. **Anonymization:** Presidio Anonymizer zamienia PII na maski
7. **Reconstruction:** Procesor odtwarza dokument z zanonimizowanym tekstem
8. **Output:** Zapisanie `.anon.docx`/`.anon.odt` i raportu JSON

## Moduły

### app/analyzer.py

**Odpowiedzialność:**
- Konfiguracja Presidio AnalyzerEngine
- Inicjalizacja SpaCy z modelem `pl_core_news_md`
- Rejestracja custom pattern recognizers dla PL_PESEL i PL_NIP

**Kluczowe funkcje:**
- `build_analyzer() -> (AnalyzerEngine, dict)` - główna funkcja zwracająca skonfigurowany analyzer
- `_add_custom_recognizers(analyzer, config)` - dodaje niestandardowe rozpoznawacze
- `get_supported_entities(config) -> list[str]` - zwraca listę obsługiwanych encji

**Używane biblioteki:**
- `presidio-analyzer` - główny engine wykrywania PII
- `spacy` - NLP dla języka polskiego

**Decyzje projektowe:**
- SpaCy został wybrany jako backend NLP ze względu na dobre wsparcie dla języka polskiego
- Custom recognizers używają wyrażeń regularnych dla PESEL/NIP (prostsze i szybsze niż ML)

### app/anonymizer.py

**Odpowiedzialność:**
- Anonimizacja tekstu na podstawie wyników z Analyzer
- Generowanie raportów statystycznych

**Kluczowe funkcje:**
- `anonymize_text(text, results, config) -> str` - główna funkcja anonimizacji
- `prepare_anonymization_report(results, config) -> dict` - generuje raport JSON

**Używane biblioteki:**
- `presidio-anonymizer` - engine zamiany PII na maski

**Decyzje projektowe:**
- Używamy strategii "replace" (zamiana na maskę) zamiast "redact" (usunięcie)
- Logi **nigdy** nie zawierają wartości PII - tylko typy i statystyki

### app/main.py

**Odpowiedzialność:**
- Entry point aplikacji
- Parsowanie argumentów CLI
- Koordynacja procesu (wybór procesora, obsługa błędów)
- Generowanie zbiorczych raportów

**Kluczowe funkcje:**
- `main()` - główna funkcja CLI
- `anonymize_path(path, analyzer, config)` - przetwarza plik lub folder
- `_process_file(path, analyzer, config)` - wybiera odpowiedni procesor dla pliku
- `save_summary_report(reports, path)` - zapisuje raport JSONL

**Decyzje projektowe:**
- Używamy `argparse` dla CLI (standardowa biblioteka Python)
- Rekurencyjne przetwarzanie folderów (wszystkie DOCX/ODT w podfolderach)
- Exit codes: 0 = sukces, 1 = błąd

### processors/docx_processor.py

**Odpowiedzialność:**
- Przetwarzanie dokumentów Microsoft Word (DOCX)
- Anonimizacja paragrafów i tabel

**Kluczowe funkcje:**
- `process_docx(path, analyzer, config) -> (Path, dict)` - główna funkcja procesora
- `_replace_text_in_paragraph(paragraph, analyzer, config)` - anonimizuje paragraf

**Używane biblioteki:**
- `python-docx` - manipulacja dokumentami DOCX

**Decyzje projektowe (MVP):**
- **Uproszczenie formatowania:** Runs są łączone w jeden tekst przed analizą
- To powoduje utratę złożonych styli, ale upraszcza kod i przyspiesza MVP
- W przyszłych wersjach można dodać zachowanie runs (character-level replacements)

**Znane ograniczenia:**
- Style inline (bold, italic) w środku tekstu mogą się uprościć
- Hyperlinki są zachowane ale mogą stracić formatowanie
- Nie obsługuje: komentarzy, nagłówków/stopek, obiektów osadzonych

### processors/odt_processor.py

**Odpowiedzialność:**
- Przetwarzanie dokumentów LibreOffice/OpenOffice (ODT)

**Kluczowe funkcje:**
- `process_odt(path, analyzer, config) -> (Path, dict)` - główna funkcja procesora
- `_extract_all_text(doc) -> str` - ekstrahuje cały tekst z dokumentu

**Używane biblioteki:**
- `odfpy` - manipulacja dokumentami ODF

**Decyzje projektowe (MVP):**
- **Maksymalne uproszczenie:** Cały dokument jest linearyzowany (ekstrakcja tekstu)
- Anonimizowany tekst jest zapisywany jako nowy prosty dokument ODT
- Struktura i formatowanie nie są zachowane

**Znane ograniczenia:**
- Cała struktura dokumentu jest tracona (tabele, listy, formatowanie)
- To jest świadomy trade-off dla MVP - pełne zachowanie struktury ODT jest skomplikowane
- W przyszłych wersjach można dodać zachowanie struktury (node-level processing)

## Konfiguracja

### config/entities.yaml

Format konfiguracji encji:

```yaml
language: pl           # Język dokumentów
threshold: 0.35        # Próg pewności detekcji (0.0 - 1.0)

entities:
  ENTITY_NAME:
    mask: "[MASKA]"                  # Tekst zamieniający
    description: "Opis encji"        # Dokumentacja
    patterns:                        # Opcjonalne wzorce regex
      - name: "PATTERN_NAME"
        regex: '\bregex_pattern\b'
        score: 0.6                   # Pewność dla tego wzorca
```

**Jak działa threshold:**
- Presidio przypisuje score (0.0 - 1.0) każdemu wykryciu
- Tylko wykrycia z score >= threshold są zwracane
- Niższy threshold = więcej wykryć (ale więcej false positives)
- Wyższy threshold = mniej wykryć (mniej false positives, ale też false negatives)

### config/logging.yaml

Standardowa konfiguracja logowania Python (format dict config).

**Handlery:**
- `console` - stdout, poziom INFO
- `file` - rotating file (10MB, 3 backupy), poziom DEBUG

**Loggery:**
- `presidio` - biblioteka Presidio
- `app` - nasza aplikacja

**⚠️ BEZPIECZEŃSTWO:** Logi są filtrowane aby nie zawierały wartości PII

## Zależności

### Python packages

| Pakiet | Wersja | Cel |
|--------|--------|-----|
| presidio-analyzer | 2.2.354 | Wykrywanie PII |
| presidio-anonymizer | 2.2.354 | Anonimizacja PII |
| spacy | 3.7.2 | NLP engine |
| python-docx | 1.1.0 | Obsługa DOCX |
| odfpy | 1.4.1 | Obsługa ODT |
| pyyaml | 6.0.1 | Parsowanie YAML |

### Dodatkowe zasoby

- **Model SpaCy:** `pl_core_news_md` - model średniej wielkości dla języka polskiego
  - Rozmiar: ~50 MB
  - Zawiera: tokenizer, tagger, parser, NER
  - Trenowany na: Wikipedia, OpenSubtitles, ParaCrawl

## Instalacja (wewnętrzne szczegóły)

### Co robi skrypt install.ps1

1. **Weryfikacja środowiska:**
   - Sprawdza czy winget jest dostępny
   - Sprawdza uprawnienia użytkownika

2. **Instalacja narzędzi:**
   - Python 3.11 (przez winget)
   - Git (przez winget)

3. **Przygotowanie aplikacji:**
   - Klonuje repo do `%LOCALAPPDATA%\PresidioAnon\app`
   - Tworzy venv w `.venv`
   - Instaluje zależności przez pip

4. **Integracja z systemem:**
   - Tworzy wrapper script `bin\anonymize.cmd`
   - Dodaje `bin\` do PATH użytkownika
   - Rejestruje menu kontekstowe w HKCU (nie wymaga admin)

5. **Smoke test:**
   - Próbuje przetworzyć przykładowy plik testowy

### Struktura instalacji

```
%LOCALAPPDATA%\PresidioAnon\
├── app\                           # Sklonowane repozytorium
│   ├── .git\
│   ├── .venv\                     # Środowisko wirtualne Python
│   ├── app\                       # Kod aplikacji
│   ├── processors\
│   ├── config\
│   ├── scripts\
│   └── ...
└── bin\
    └── anonymize.cmd              # Wrapper script
```

## Wydajność

### Benchmarki (orientacyjne)

**Testowane na:** Windows 11, i7-8700K, 16GB RAM, SSD

| Scenariusz | Czas | Pamięć |
|------------|------|--------|
| Dokument 1 strona (10 wykryć) | ~3s | ~300 MB |
| Dokument 10 stron (100 wykryć) | ~8s | ~400 MB |
| Folder 50 plików | ~3 min | ~500 MB |

**Wąskie gardła:**
- Inicjalizacja modelu SpaCy (~2s przy pierwszym użyciu)
- Analiza NLP (większość czasu)
- I/O (czytanie/zapisywanie dokumentów)

### Możliwe optymalizacje (przyszłe wersje)

- Cache'owanie modelu SpaCy między wywołaniami
- Przetwarzanie równoległe wielu plików
- Batch processing dla wielu tekstów (Presidio batch API)
- Lazy loading dokumentów (streaming)

## Testowanie

### Unit testy (TODO)

Przyszłe testy powinny pokryć:
- `app/analyzer.py` - konfiguracja analyzera
- `app/anonymizer.py` - logika anonimizacji
- Pattern recognizers - regex dla PESEL/NIP

### Integration testy (TODO)

- End-to-end test na przykładowym dokumencie
- Test wsadowy (folder z wieloma plikami)
- Test edge cases (pusty dokument, dokument bez PII)

### Manualne testowanie

Zobacz: `tests/expected_results.md`

## Znane problemy i ograniczenia

### False positives

**Problem:** System wykrywa jako PERSON zwykłe słowa

**Przykład:** "Projekt Kowalski" → wykrywane jako osoba

**Rozwiązanie:** Zwiększ threshold lub dostosuj model NLP

### False negatives

**Problem:** System nie wykrywa niektórych PII

**Przykład:** Nietypowe formaty PESEL/NIP ze spacjami

**Rozwiązanie:** Dodaj dodatkowe wzorce regex w konfiguracji

### Formatowanie DOCX

**Problem:** Style inline są uproszczane

**Przykład:** "Jan **Kowalski**" → "[OSOBA]" (tracony bold)

**Przyczyna:** MVP łączy runs przed analizą

**Roadmap:** v0.2.0 - character-level replacement

### Struktura ODT

**Problem:** Cała struktura dokumentu jest linearyzowana

**Przyczyna:** Pełne zachowanie struktury ODF jest bardzo złożone

**Roadmap:** v0.3.0 - zachowanie podstawowej struktury

## Bezpieczeństwo

### Threat model

**Zagrożenia:**
- Przypadkowe wyciek PII w logach → **Mitigated** (logi filtrowane)
- Niekompletna anonimizacja → **Accepted risk** (100% pewności nie da się osiągnąć)
- Zła konfiguracja przez użytkownika → **User responsibility**

### Najlepsze praktyki

✅ Zawsze weryfikuj wyniki przed publikacją
✅ Używaj wysokiego threshold dla dokumentów o krytycznym znaczeniu
✅ Testuj na próbkach przed przetworzeniem całego zbioru
✅ Przechowuj oryginały jako backup

## Rozwój

### Jak dodać wsparcie dla nowego formatu?

1. Utwórz nowy processor w `processors/`
2. Implementuj funkcję `process_FORMAT(path, analyzer, config)`
3. Dodaj logikę wyboru w `app/main.py::_process_file()`

### Jak dodać nową encję?

1. Dodaj definicję w `config/entities.yaml`
2. Jeśli używa regex: dodaj patterns
3. Jeśli używa ML: dostosuj model SpaCy lub Presidio recognizer

### Kontrybucje

Zobacz: `docs/CONTRIBUTING.md` (TODO)

## FAQ

**Q: Czy aplikacja wysyła dane do internetu?**
A: Nie. Całość działa offline.

**Q: Czy mogę używać na dokumentach firmowych?**
A: Tak, ale zawsze weryfikuj wyniki. Nie dajemy gwarancji 100% skuteczności.

**Q: Czy działa na macOS/Linux?**
A: Obecnie tylko Windows. macOS/Linux w roadmapie.

**Q: Czy mogę używać komercyjnie?**
A: Tak, licencja MIT pozwala na użytek komercyjny.

---

**Wersja dokumentacji:** 0.1.0 (2024-12-10)
