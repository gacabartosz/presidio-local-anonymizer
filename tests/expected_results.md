# Oczekiwane wyniki testów

## Test podstawowy - dokument z pełnymi danymi

### Dane wejściowe
- Plik: `test_document.docx`
- Zawiera: 3 osoby, 3 emaile, 3 telefony, 3 PESEL, 2 NIP

### Oczekiwane wykrycia

| Typ encji       | Oczekiwana liczba | Przykładowe wartości                              |
|-----------------|-------------------|---------------------------------------------------|
| PERSON          | 3                 | Jan Kowalski, Anna Nowak, Piotr Wiśniewski       |
| EMAIL_ADDRESS   | 3                 | jan.kowalski@example.com, anna.nowak@firma.pl    |
| PHONE_NUMBER    | 3                 | +48 123 456 789, 505 123 456, 600 789 123        |
| PL_PESEL        | 3                 | 92010212345, 85032198765, 78121567890            |
| PL_NIP          | 2                 | 123-456-78-90, 9876543210                        |

**Łącznie: 14 wykryć**

### Oczekiwany raport JSON

```json
{
  "source_file": "path/to/test_document.docx",
  "output_file": "path/to/test_document.anon.docx",
  "status": "success",
  "timestamp": "2024-XX-XXTXX:XX:XX",
  "format": "DOCX",
  "analysis": {
    "total_detections": 14,
    "entities": {
      "PERSON": {
        "count": 3,
        "mask": "[OSOBA]",
        "avg_score": 0.85
      },
      "EMAIL_ADDRESS": {
        "count": 3,
        "mask": "[EMAIL]",
        "avg_score": 1.0
      },
      "PHONE_NUMBER": {
        "count": 3,
        "mask": "[TELEFON]",
        "avg_score": 0.7
      },
      "PL_PESEL": {
        "count": 3,
        "mask": "[PESEL]",
        "avg_score": 0.6
      },
      "PL_NIP": {
        "count": 2,
        "mask": "[NIP]",
        "avg_score": 0.75
      }
    },
    "threshold_used": 0.35
  }
}
```

### Oczekiwany dokument wyjściowy

Tekst powinien wyglądać tak:

```
System Anonimizacji Dokumentów - Test

Dane osobowe do wykrycia:

Imię i nazwisko: [OSOBA]
Email: [EMAIL]
Telefon: [TELEFON]
PESEL: [PESEL]
NIP: [NIP]

Dodatkowe dane:
Imię i nazwisko: [OSOBA]
Email: [EMAIL]
Telefon: [TELEFON]
PESEL: [PESEL]
NIP: [NIP]

Tabela z danymi:

| Osoba    | Email   | Telefon    | PESEL    |
|----------|---------|------------|----------|
| [OSOBA]  | [EMAIL] | [TELEFON]  | [PESEL]  |
| [OSOBA]  | [EMAIL] | [TELEFON]  | [PESEL]  |
| [OSOBA]  | [EMAIL] | [TELEFON]  | [PESEL]  |

Test zakończony.
```

## Test z pustym dokumentem

### Dane wejściowe
- Plik: `empty_document.docx`
- Zawiera: tylko tekst bez danych osobowych

### Oczekiwane wyniki
- `total_detections`: 0
- `entities`: {}
- Dokument wyjściowy identyczny z wejściowym (poza możliwymi zmianami formatowania w MVP)

## Test wsadowy (folder)

### Dane wejściowe
- Folder: `test_batch/` zawierający 5 plików DOCX i 3 pliki ODT

### Oczekiwane wyniki
- Przetworzono 8 plików
- Wygenerowano 8 plików `.anon.docx` / `.anon.odt`
- Wygenerowano 8 raportów `.anon.json`
- Zbiorczy raport `summary.jsonl` (jeśli podano parametr --report)

## Typowe problemy i rozwiązania

### Problem: False positives (fałszywe wykrycia)

**Symptom:** System wykrywa jako PERSON zwykłe słowa niepowiązane z osobami

**Przykład:** "Projekt Kowalski" wykrywane jako osoba

**Rozwiązanie:**
- Dostosuj threshold w `config/entities.yaml`
- Wyższy threshold = mniej fałszywych wykryć, ale też mniej prawdziwych wykryć

### Problem: Brak wykrycia polskich PESEL/NIP

**Symptom:** System nie wykrywa numerów PESEL lub NIP

**Możliwe przyczyny:**
- PESEL/NIP w nietypowym formacie (z spacjami, kropkami)
- Wzorzec regex w konfiguracji nie pasuje do formatu

**Rozwiązanie:**
- Zaktualizuj wzorce regex w `config/entities.yaml`
- Dodaj dodatkowe wzorce dla różnych formatów

### Problem: Zły model językowy

**Symptom:** System słabo wykrywa polskie imiona i nazwiska

**Rozwiązanie:**
- Upewnij się że model SpaCy `pl_core_news_md` jest zainstalowany
- Sprawdź: `python -m spacy validate`

## Metryki wydajności

Dla dokumentu testowego (~1 strona, 14 wykryć):
- Czas przetwarzania: < 5 sekund
- Rozmiar pliku wyjściowego: podobny do wejściowego
- Użycie pamięci: < 500 MB

Dla folderu (100 dokumentów, ~1000 wykryć łącznie):
- Czas przetwarzania: < 5 minut
- Przetwarzanie sekwencyjne (nie równoległe w MVP)
