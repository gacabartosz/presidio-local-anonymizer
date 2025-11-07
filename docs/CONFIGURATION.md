# Poradnik konfiguracji

## Przegląd

System anonimizacji jest w pełni konfigurowalny przez pliki YAML. Możesz dostosować:
- Wykrywane typy danych osobowych
- Maski zastępujące
- Wzorce wykrywania (regex)
- Progi pewności detekcji

## Lokalizacja plików konfiguracyjnych

Pliki znajdują się w:
```
%LOCALAPPDATA%\PresidioAnon\app\config\
├── entities.yaml    # Konfiguracja encji i masek
└── logging.yaml     # Konfiguracja logowania
```

## Plik entities.yaml

### Struktura podstawowa

```yaml
language: pl           # Język dokumentów
threshold: 0.35        # Globalny próg pewności (0.0 - 1.0)

entities:
  ENTITY_NAME:         # Nazwa encji (uppercase)
    mask: "[MASKA]"    # Tekst zastępujący PII
    description: "Opis encji"
```

### Parametry globalne

#### language

Określa język dokumentów do przetwarzania.

```yaml
language: pl    # Polski
language: en    # Angielski
```

#### threshold

Globalny próg pewności dla wszystkich detekcji (0.0 - 1.0).

```yaml
threshold: 0.35    # Domyślne - balans między czułością a precyzją
threshold: 0.50    # Wyższe - mniej false positives, ale też mniej wykryć
threshold: 0.20    # Niższe - więcej wykryć, ale więcej false positives
```

**Jak wybrać threshold:**
- **0.20-0.30** - Dokumenty wewnętrzne, draft - wolisz wykryć wszystko
- **0.35-0.45** - Dokumenty standardowe - balans
- **0.50-0.70** - Dokumenty publiczne, krytyczne - minimalizujesz false positives

### Konfiguracja encji

#### Encje wbudowane (Presidio)

Te encje są rozpoznawane automatycznie przez Presidio + SpaCy:

```yaml
entities:
  PERSON:
    mask: "[OSOBA]"
    description: "Imię i nazwisko osoby"

  EMAIL_ADDRESS:
    mask: "[EMAIL]"
    description: "Adres email"

  PHONE_NUMBER:
    mask: "[TELEFON]"
    description: "Numer telefonu"

  LOCATION:
    mask: "[LOKALIZACJA]"
    description: "Lokalizacja geograficzna"

  DATE_TIME:
    mask: "[DATA]"
    description: "Data lub data i czas"

  URL:
    mask: "[URL]"
    description: "Adres URL"

  IP_ADDRESS:
    mask: "[IP]"
    description: "Adres IP"
```

#### Encje niestandardowe (Pattern-based)

Dla encji specyficznych dla Polski lub branży możesz dodać własne wzorce regex:

```yaml
  PL_PESEL:
    mask: "[PESEL]"
    description: "Polski numer PESEL"
    patterns:
      - name: "PESEL_PATTERN"
        regex: '\b\d{11}\b'
        score: 0.6

  PL_NIP:
    mask: "[NIP]"
    description: "Polski numer NIP"
    patterns:
      - name: "NIP_WITH_DASHES"
        regex: '\b\d{3}-\d{3}-\d{2}-\d{2}\b'
        score: 0.8
      - name: "NIP_NO_DASHES"
        regex: '\b\d{10}\b'
        score: 0.5
```

**Parametry pattern:**
- `name` - Unikalna nazwa wzorca (dla logów)
- `regex` - Wyrażenie regularne (Python flavor)
- `score` - Pewność dla tego wzorca (0.0 - 1.0)

### Przykłady zastosowań

#### Przykład 1: Dodanie polskiego dowodu osobistego

```yaml
  PL_ID_CARD:
    mask: "[DOWÓD]"
    description: "Polski numer dowodu osobistego"
    patterns:
      - name: "ID_CARD_NEW_FORMAT"
        regex: '\b[A-Z]{3}\s?\d{6}\b'
        score: 0.7
```

**Wykryje:** ABC 123456, ABC123456

#### Przykład 2: Dodanie firmowego ID pracownika

```yaml
  EMPLOYEE_ID:
    mask: "[ID_PRACOWNIKA]"
    description: "Wewnętrzny numer pracownika"
    patterns:
      - name: "EMPLOYEE_ID_FORMAT"
        regex: '\bEMP-\d{5}\b'
        score: 0.9
```

**Wykryje:** EMP-12345

#### Przykład 3: Numer konta bankowego (IBAN)

```yaml
  PL_IBAN:
    mask: "[KONTO]"
    description: "Polski numer konta bankowego (IBAN)"
    patterns:
      - name: "IBAN_PL"
        regex: '\bPL\d{26}\b'
        score: 0.95
      - name: "IBAN_PL_WITH_SPACES"
        regex: '\bPL\s?\d{2}\s?\d{4}\s?\d{4}\s?\d{4}\s?\d{4}\s?\d{4}\s?\d{4}\b'
        score: 0.95
```

**Wykryje:** PL61109010140000071219812874, PL 61 1090 1014 0000 0712 1981 2874

#### Przykład 4: Numer paszportu

```yaml
  PL_PASSPORT:
    mask: "[PASZPORT]"
    description: "Polski numer paszportu"
    patterns:
      - name: "PASSPORT_FORMAT"
        regex: '\b[A-Z]{2}\d{7}\b'
        score: 0.8
```

**Wykryje:** AA1234567

#### Przykład 5: Numer karty płatniczej (częściowy)

```yaml
  CREDIT_CARD:
    mask: "[KARTA]"
    description: "Numer karty płatniczej"
    patterns:
      - name: "CARD_16_DIGITS"
        regex: '\b\d{4}[\s-]?\d{4}[\s-]?\d{4}[\s-]?\d{4}\b'
        score: 0.6
```

**Wykryje:** 1234 5678 9012 3456, 1234-5678-9012-3456

### Dostosowanie masek

Możesz zmienić sposób maskowania:

```yaml
# Opcja 1: Opisowe maski (domyślne)
entities:
  PERSON:
    mask: "[OSOBA]"
  EMAIL_ADDRESS:
    mask: "[EMAIL]"

# Opcja 2: Generyczne redakcje
entities:
  PERSON:
    mask: "[REDACTED]"
  EMAIL_ADDRESS:
    mask: "[REDACTED]"

# Opcja 3: Symbole
entities:
  PERSON:
    mask: "***"
  EMAIL_ADDRESS:
    mask: "***"

# Opcja 4: Numerowane
entities:
  PERSON:
    mask: "[PII-1]"
  EMAIL_ADDRESS:
    mask: "[PII-2]"

# Opcja 5: Custom text
entities:
  PERSON:
    mask: "<Imię i nazwisko usunięte>"
  EMAIL_ADDRESS:
    mask: "<Email usunięty>"
```

### Wyłączanie encji

Jeśli nie chcesz wykrywać określonej encji, po prostu usuń jej definicję z pliku.

**Przykład:** Wykrywaj tylko emaile i telefony

```yaml
language: pl
threshold: 0.35

entities:
  EMAIL_ADDRESS:
    mask: "[EMAIL]"
    description: "Adres email"

  PHONE_NUMBER:
    mask: "[TELEFON]"
    description: "Numer telefonu"
```

### Pisanie wyrażeń regularnych

#### Podstawowe elementy regex

```regex
\b        # Granica słowa (word boundary)
\d        # Cyfra (0-9)
\d{11}    # Dokładnie 11 cyfr
\d{3,5}   # Od 3 do 5 cyfr
[A-Z]     # Wielka litera (A-Z)
[a-z]     # Mała litera (a-z)
[\s-]?    # Opcjonalna spacja lub myślnik
.         # Dowolny znak (użyj \. dla kropki literalnej)
^         # Początek linii
$         # Koniec linii
```

#### Przykłady wzorców

**PESEL (11 cyfr):**
```regex
\b\d{11}\b
```

**PESEL z spacjami (YY MM DD XXXXX):**
```regex
\b\d{2}\s\d{2}\s\d{2}\s\d{5}\b
```

**NIP (różne formaty):**
```regex
# Format: 123-456-78-90
\b\d{3}-\d{3}-\d{2}-\d{2}\b

# Format: 123-45-67-890
\b\d{3}-\d{2}-\d{2}-\d{3}\b

# Format: 1234567890 (bez separatorów)
\b\d{10}\b
```

**Email (uproszczony):**
```regex
\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b
```

**Polski telefon:**
```regex
# Format: +48 123 456 789
\+48\s?\d{3}\s?\d{3}\s?\d{3}

# Format: 123-456-789
\d{3}-\d{3}-\d{3}

# Format: 123456789
\b\d{9}\b
```

#### Testowanie regex

Użyj narzędzi online do testowania:
- https://regex101.com/ (wybierz flavor: Python)
- https://regexr.com/

**Przykład testowania PESEL:**
1. Wejdź na regex101.com
2. Wybierz flavor: Python
3. Wpisz regex: `\b\d{11}\b`
4. Test string: "Mój PESEL to 92010212345 a NIP to 1234567890"
5. Sprawdź czy wykrywa 92010212345

### Score (pewność) dla wzorców

Parametr `score` określa jak pewny jest system że wykrycie jest prawidłowe.

```yaml
patterns:
  - name: "VERY_SPECIFIC_PATTERN"
    regex: '\bPL\d{26}\b'
    score: 0.95    # Bardzo specyficzny format (IBAN) - wysoka pewność

  - name: "GENERIC_PATTERN"
    regex: '\b\d{10}\b'
    score: 0.4     # Ogólny format (10 cyfr) - niska pewność (może być cokolwiek)
```

**Zasady wyboru score:**
- **0.9-1.0** - Bardzo specyficzne formaty (IBAN, specjalne prefiksy)
- **0.7-0.8** - Specyficzne formaty z checksumami lub strukturą (NIP z myślnikami)
- **0.5-0.6** - Podstawowe formaty (PESEL, NIP bez separatorów)
- **0.3-0.4** - Ogólne wzorce które mogą mieć false positives

### Walidacja konfiguracji

Po edycji `entities.yaml` możesz sprawdzić poprawność:

```bash
# Uruchom z verbose mode aby zobaczyć załadowane encje
anonymize.cmd test_document.docx --verbose
```

W logach powinna pojawić się linia:
```
Analyzer gotowy. Obsługiwane encje: ['PERSON', 'EMAIL_ADDRESS', 'PL_PESEL', ...]
```

### Przykładowe konfiguracje

#### Konfiguracja "Minimalna" (tylko krytyczne dane)

```yaml
language: pl
threshold: 0.5

entities:
  PERSON:
    mask: "[OSOBA]"
  EMAIL_ADDRESS:
    mask: "[EMAIL]"
  PL_PESEL:
    mask: "[PESEL]"
    patterns:
      - name: "PESEL_PATTERN"
        regex: '\b\d{11}\b'
        score: 0.6
```

#### Konfiguracja "Maksymalna" (wszystkie możliwe dane)

```yaml
language: pl
threshold: 0.30

entities:
  PERSON:
    mask: "[OSOBA]"
  EMAIL_ADDRESS:
    mask: "[EMAIL]"
  PHONE_NUMBER:
    mask: "[TELEFON]"
  PL_PESEL:
    mask: "[PESEL]"
    patterns:
      - name: "PESEL_PATTERN"
        regex: '\b\d{11}\b'
        score: 0.6
  PL_NIP:
    mask: "[NIP]"
    patterns:
      - name: "NIP_WITH_DASHES"
        regex: '\b\d{3}-\d{3}-\d{2}-\d{2}\b'
        score: 0.8
      - name: "NIP_NO_DASHES"
        regex: '\b\d{10}\b'
        score: 0.5
  PL_ID_CARD:
    mask: "[DOWÓD]"
    patterns:
      - name: "ID_CARD_FORMAT"
        regex: '\b[A-Z]{3}\s?\d{6}\b'
        score: 0.7
  PL_IBAN:
    mask: "[KONTO]"
    patterns:
      - name: "IBAN_PL"
        regex: '\bPL\d{26}\b'
        score: 0.95
  LOCATION:
    mask: "[LOKALIZACJA]"
  DATE_TIME:
    mask: "[DATA]"
  URL:
    mask: "[URL]"
  IP_ADDRESS:
    mask: "[IP]"
```

#### Konfiguracja "Firmowa" (dane pracowników)

```yaml
language: pl
threshold: 0.40

entities:
  PERSON:
    mask: "[OSOBA]"
  EMAIL_ADDRESS:
    mask: "[EMAIL]"
  PHONE_NUMBER:
    mask: "[TELEFON]"

  EMPLOYEE_ID:
    mask: "[ID_PRACOWNIKA]"
    patterns:
      - name: "EMPLOYEE_ID"
        regex: '\bEMP-\d{5}\b'
        score: 0.95

  DEPARTMENT_CODE:
    mask: "[KOD_DZIAŁU]"
    patterns:
      - name: "DEPT_CODE"
        regex: '\bDEPT-[A-Z]{2,4}\b'
        score: 0.9

  SALARY_INFO:
    mask: "[WYNAGRODZENIE]"
    patterns:
      - name: "SALARY_PLN"
        regex: '\b\d{4,6}\s?PLN\b'
        score: 0.5
```

## Plik logging.yaml

### Dostosowanie poziomu logowania

```yaml
loggers:
  presidio:
    level: INFO      # DEBUG, INFO, WARNING, ERROR
  app:
    level: INFO
```

### Zmiana lokalizacji logów

```yaml
handlers:
  file:
    filename: C:\Custom\Path\anonymizer.log  # Twoja ścieżka
```

### Wyłączenie logowania do pliku

Usuń handler `file` z sekcji loggers:

```yaml
loggers:
  app:
    level: INFO
    handlers: [console]    # Tylko konsola, bez file
    propagate: false
```

## Najlepsze praktyki

✅ **Backupuj konfigurację** przed edycją
✅ **Testuj na małych plikach** po zmianie konfiguracji
✅ **Dokumentuj zmiany** - dodawaj komentarze w YAML
✅ **Używaj verbose mode** (`--verbose`) do debugowania
✅ **Sprawdzaj logi** po pierwszym uruchomieniu z nową konfiguracją

## Troubleshooting

### Problem: Encja nie jest wykrywana

**Rozwiązanie:**
1. Sprawdź czy encja jest w `entities.yaml`
2. Użyj `--verbose` i sprawdź logi
3. Obniż threshold
4. Dla custom patterns: przetestuj regex na regex101.com

### Problem: Za dużo false positives

**Rozwiązanie:**
1. Zwiększ threshold
2. Zwiększ score dla wzorca regex
3. Użyj bardziej specyficznego regex (dodaj context)

### Problem: Za mało wykryć

**Rozwiązanie:**
1. Obniż threshold
2. Dodaj dodatkowe wzorce regex dla różnych formatów
3. Sprawdź czy model SpaCy jest zainstalowany

### Problem: Nieprawidłowy YAML

**Objawy:** Błąd podczas uruchamiania `yaml.parser.ParserError`

**Rozwiązanie:**
1. Sprawdź wcięcia (muszą być spacjami, nie tabami)
2. Sprawdź cudzysłowy w stringach z znakami specjalnymi
3. Użyj walidatora YAML online: https://www.yamllint.com/

---

**Wersja:** 0.1.0
