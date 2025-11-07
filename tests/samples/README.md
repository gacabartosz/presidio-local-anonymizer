# Pliki testowe

Ten folder zawiera przykładowe dokumenty do testowania systemu anonimizacji.

## Tworzenie plików testowych

### Test Document DOCX

Utwórz plik `test_document.docx` w Microsoft Word lub LibreOffice Writer z następującą zawartością:

```
System Anonimizacji Dokumentów - Test

Dane osobowe do wykrycia:

Imię i nazwisko: Jan Kowalski
Email: jan.kowalski@example.com
Telefon: +48 123 456 789
PESEL: 92010212345
NIP: 123-456-78-90

Dodatkowe dane:
Imię i nazwisko: Anna Nowak
Email: anna.nowak@firma.pl
Telefon: 505 123 456
PESEL: 85032198765
NIP: 9876543210

Tabela z danymi:

| Osoba          | Email                    | Telefon         | PESEL         |
|----------------|--------------------------|-----------------|---------------|
| Jan Kowalski   | jan.kowalski@example.com | +48 123 456 789 | 92010212345   |
| Anna Nowak     | anna.nowak@firma.pl      | 505 123 456     | 85032198765   |
| Piotr Wiśniewski | piotr.w@test.com       | 600 789 123     | 78121567890   |

Test zakończony.
```

### Test Document ODT

Utwórz plik `test_document.odt` w LibreOffice Writer z podobną zawartością.

## Oczekiwane wyniki

Po przetworzeniu dokumentu, system powinien:

1. **Wykryć następujące encje:**
   - PERSON: Jan Kowalski, Anna Nowak, Piotr Wiśniewski (3 wystąpienia)
   - EMAIL_ADDRESS: jan.kowalski@example.com, anna.nowak@firma.pl, piotr.w@test.com (3 wystąpienia)
   - PHONE_NUMBER: +48 123 456 789, 505 123 456, 600 789 123 (3 wystąpienia)
   - PL_PESEL: 92010212345, 85032198765, 78121567890 (3 wystąpienia)
   - PL_NIP: 123-456-78-90, 9876543210 (2 wystąpienia)

2. **Zamaskować je następująco:**
   - PERSON → `[OSOBA]`
   - EMAIL_ADDRESS → `[EMAIL]`
   - PHONE_NUMBER → `[TELEFON]`
   - PL_PESEL → `[PESEL]`
   - PL_NIP → `[NIP]`

3. **Wygenerować pliki:**
   - `test_document.anon.docx` - zanonimizowany dokument
   - `test_document.anon.json` - raport z analizy

4. **Raport JSON powinien zawierać:**
   - `source_file`: ścieżka do oryginalnego pliku
   - `output_file`: ścieżka do zanonimizowanego pliku
   - `status`: "success"
   - `timestamp`: data i czas przetworzenia
   - `format`: "DOCX" lub "ODT"
   - `analysis`: statystyki wykrytych encji
     - `total_detections`: łączna liczba wykryć
     - `entities`: szczegóły dla każdego typu encji
       - `count`: liczba wystąpień
       - `mask`: zastosowana maska
       - `avg_score`: średni poziom pewności

## Dodatkowe testy

### Test z folderem

1. Utwórz folder `test_batch/`
2. Dodaj kilka plików DOCX i ODT
3. Uruchom: `anonymize.cmd test_batch/`
4. Sprawdź czy wszystkie pliki zostały przetworzone

### Test z danymi bez PII

Utwórz dokument bez danych osobowych i sprawdź czy:
- System nie wykrywa żadnych encji
- Dokument wyjściowy jest identyczny z wejściowym (poza możliwymi zmianami formatowania)

### Test z różnymi formatami numerów

Przetestuj różne formaty:
- PESEL: 92010212345, 92 01 02 12345
- NIP: 123-456-78-90, 123-45-67-890, 1234567890
- Telefon: +48 123 456 789, 48123456789, 123456789, 123-456-789

## Weryfikacja działania

Po przetworzeniu otwórz plik `.anon.docx` i zweryfikuj:
- ✓ Wszystkie dane osobowe zostały zamaskowane
- ✓ Struktura dokumentu została zachowana
- ✓ Tabele są poprawnie przetworzone
- ✓ Nie ma przypadkowych wykryć (false positives)
