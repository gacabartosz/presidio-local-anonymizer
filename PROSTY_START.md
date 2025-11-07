# 🚀 PROSTY START - Dla Każdego

**Dla osób które chcą po prostu URUCHOMIĆ aplikację bez komplikacji.**

---

## 📱 METODA 1: Quick Start (NAJŁATWIEJSZE)

**Jedna komenda - instaluje i uruchamia GUI:**

### macOS/Linux:

```bash
bash <(curl -fsSL https://raw.githubusercontent.com/gacabartosz/presidio-local-anonymizer/main/quick-start.sh)
```

**Co robi:**
1. Sprawdza czy aplikacja jest zainstalowana
2. Jeśli NIE - automatycznie instaluje
3. Uruchamia interfejs graficzny (GUI)

✅ **To wszystko! Jedna komenda i masz działającą aplikację.**

---

## 📥 METODA 2: Standalone Installer (NAJBEZPIECZNIEJSZE)

**Pobierz plik, sprawdź, uruchom:**

### Krok 1: Pobierz installer

```bash
curl -O https://raw.githubusercontent.com/gacabartosz/presidio-local-anonymizer/main/install-standalone.sh
```

### Krok 2: Sprawdź zawartość (opcjonalnie)

```bash
less install-standalone.sh  # Przejrzyj kod
```

### Krok 3: Uruchom

```bash
bash install-standalone.sh
```

### Krok 4: Po instalacji

```bash
# Otwórz NOWE okno terminala, potem:
anonymize-gui
```

---

## 🆘 METODA 3: Jeśli żadna nie działa

**Pełna instalacja ręczna krok po kroku:**

👉 **[MANUAL_INSTALL.md](MANUAL_INSTALL.md)** - 12 prostych kroków

Każdy krok pokazuje:
- Co wpisać
- Co powinno się pojawić
- Jak sprawdzić czy działa

---

## ❓ FAQ - Szybkie Pytania

### Q: Która metoda jest najlepsza?

**A:** METODA 1 (quick-start.sh) - najszybsza, wszystko automatycznie.

### Q: Czy to bezpieczne?

**A:** TAK. Wszystkie skrypty są:
- Dostępne do wglądu na GitHub
- Open source (licencja MIT)
- Instalują tylko oficjalne pakiety
- Działają lokalnie (bez wysyłania danych)

### Q: Co jeśli nie działa?

**A:** Wypróbuj w kolejności:
1. **METODA 2** (install-standalone.sh) - bardziej niezawodna
2. **[MANUAL_INSTALL.md](MANUAL_INSTALL.md)** - ręczna instalacja
3. **[TROUBLESHOOTING.md](TROUBLESHOOTING.md)** - rozwiązywanie problemów

### Q: Jak długo to trwa?

**A:**
- Pierwsza instalacja: **10-15 minut**
- Kolejne uruchomienia: **natychmiast**

### Q: Czy muszę mieć dostęp administratora?

**A:**
- **macOS:** NIE (ale Homebrew może zapytać o hasło - to normalne!)
- **Linux:** TAK (dla apt-get install)

### Q: Czy działa offline?

**A:**
- Instalacja: **NIE** (musi pobrać pakiety)
- Po instalacji: **TAK** (100% offline)

---

## 🎯 Po Instalacji

### Jak uruchomić aplikację:

**Interfejs graficzny (najłatwiejszy):**
```bash
anonymize-gui
```

**Z linii poleceń:**
```bash
anonymize dokument.docx
```

**Prawy przycisk myszy (macOS):**
1. Kliknij prawym na pliku
2. Quick Actions → Anonimizuj (Presidio)

---

## 📞 Potrzebujesz Pomocy?

1. **[TROUBLESHOOTING.md](TROUBLESHOOTING.md)** - Rozwiązywanie problemów
2. **[MANUAL_INSTALL.md](MANUAL_INSTALL.md)** - Instalacja ręczna
3. **[GitHub Issues](https://github.com/gacabartosz/presidio-local-anonymizer/issues)** - Zgłoś problem

---

## ✅ Sprawdź czy działa

Po instalacji sprawdź:

```bash
# Sprawdź wersję
anonymize --help

# Uruchom GUI
anonymize-gui

# Test na pliku
echo "Jan Kowalski, email: test@example.com" > ~/Desktop/test.txt
anonymize ~/Desktop/test.txt
cat ~/Desktop/test.anon.txt  # Powinny być ukryte dane
```

---

## 🔐 Bezpieczeństwo

✅ Wszystko działa **lokalnie** na Twoim komputerze
✅ Żadne dane **nie są wysyłane** przez internet
✅ Kod jest **open source** - możesz sprawdzić
✅ Używa tylko **oficjalnych** pakietów (Homebrew, PyPI)

---

👨‍💻 Created by [bartoszgaca.pl](https://bartoszgaca.pl) & 🤖 [Claude Code](https://claude.com/claude-code)
