# 🐛 Fix: SpaCy Model Download Error 404

## ❌ Problem

**Błąd podczas instalacji:**
```
ERROR: HTTP error 404 while getting
https://github.com/explosion/spacy-models/releases/download/-pl_core_news_md/-pl_core_news_md.tar.gz
```

## 🔍 Diagnoza

**Przyczyna:**
- Komenda `python -m spacy download pl_core_news_md` nie działa poprawnie ze SpaCy 3.7.2
- SpaCy próbuje znaleźć model z podwójną kreską: `-pl_core_news_md` zamiast `pl_core_news_md-3.7.0`
- URL jest nieprawidłowy, co powoduje błąd 404

**Szczegóły techniczne:**
- SpaCy w wersji 3.7.2 wymaga modelu w wersji 3.7.x
- `spacy download` automatycznie szuka odpowiedniej wersji, ale czasami się myli
- Bezpieczniejsze jest użycie bezpośredniego URL do pliku .whl

## ✅ Rozwiązanie

**NOWA METODA (po poprawce):**

Zamiast:
```bash
python -m spacy download pl_core_news_md  # ❌ Nie działa
```

Użyj:
```bash
pip install https://github.com/explosion/spacy-models/releases/download/pl_core_news_md-3.7.0/pl_core_news_md-3.7.0-py3-none-any.whl
```

## 📝 Co zostało naprawione

**Pliki zaktualizowane:**

1. **scripts/install.sh** - zmieniono metodę instalacji modelu
2. **install-standalone.sh** - zmieniono metodę instalacji modelu
3. **MANUAL_INSTALL.md** - zaktualizowano instrukcję ręczną
4. **requirements.txt** - zaktualizowano komentarz

**Zmiana:**
```diff
- python -m spacy download pl_core_news_md --quiet
+ pip install https://github.com/explosion/spacy-models/releases/download/pl_core_news_md-3.7.0/pl_core_news_md-3.7.0-py3-none-any.whl --quiet
```

## 🧪 Weryfikacja

**Jak sprawdzić czy model się zainstalował:**

```bash
# Aktywuj venv
cd ~/Library/Application\ Support/PresidioAnon/app
source .venv/bin/activate

# Sprawdź czy model jest dostępny
python -c "import spacy; nlp = spacy.load('pl_core_news_md'); print('✅ Model działa!')"
```

**Oczekiwany wynik:**
```
✅ Model działa!
```

## 📊 Dostępne wersje modelu

| Wersja SpaCy | Wersja modelu pl_core_news_md | URL |
|--------------|-------------------------------|-----|
| 3.7.x | 3.7.0 | [Download](https://github.com/explosion/spacy-models/releases/download/pl_core_news_md-3.7.0/pl_core_news_md-3.7.0-py3-none-any.whl) |
| 3.8.x | 3.8.0 | [Download](https://github.com/explosion/spacy-models/releases/download/pl_core_news_md-3.8.0/pl_core_news_md-3.8.0-py3-none-any.whl) |

## 🔗 Źródła

- **SpaCy Models GitHub:** https://github.com/explosion/spacy-models
- **Polskie modele:** https://spacy.io/models/pl
- **Compatibility matrix:** https://github.com/explosion/spacy-models/blob/master/compatibility.json

## 💡 Dla użytkowników którzy już mieli błąd

**Jeśli już próbowałeś instalować i dostałeś błąd 404:**

### Opcja 1: Pełna reinstalacja (zalecane)

```bash
# Usuń starą instalację
rm -rf ~/Library/Application\ Support/PresidioAnon

# Zainstaluj ponownie (poprawiona wersja)
bash <(curl -fsSL https://raw.githubusercontent.com/gacabartosz/presidio-local-anonymizer/main/quick-start.sh)
```

### Opcja 2: Napraw tylko model SpaCy

```bash
# Przejdź do katalogu aplikacji
cd ~/Library/Application\ Support/PresidioAnon/app

# Aktywuj środowisko
source .venv/bin/activate

# Zainstaluj model ręcznie
pip install https://github.com/explosion/spacy-models/releases/download/pl_core_news_md-3.7.0/pl_core_news_md-3.7.0-py3-none-any.whl

# Sprawdź
python -c "import spacy; spacy.load('pl_core_news_md')"
```

**Po naprawieniu:**
```bash
# Uruchom GUI
anonymize-gui

# Lub CLI
anonymize dokument.docx
```

## 🎯 Status

✅ **NAPRAWIONE** - commit: (pending)

Wszystkie skrypty instalacyjne używają teraz bezpośredniego URL do modelu.

---

👨‍💻 Created by [bartoszgaca.pl](https://bartoszgaca.pl) & 🤖 [Claude Code](https://claude.com/claude-code)
