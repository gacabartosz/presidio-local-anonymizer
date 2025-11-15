# ✨ Prosta Instalacja - Zainstaluj i Działa!

## 🚀 Instalacja w 3 krokach (bez tokenu!)

### KROK 1: Uruchom backend

```bash
cd /Users/gaca/presidio-local-anonymizer/backend
source .venv/bin/activate
python app.py
```

**Zostaw terminal otwarty!** Backend musi działać w tle.

---

### KROK 2: Załaduj extension w Chrome

1. Otwórz Chrome
2. Wejdź na: `chrome://extensions/`
3. Włącz **"Developer mode"** (prawy górny róg)
4. Kliknij **"Load unpacked"**
5. Wybierz folder: `/Users/gaca/presidio-local-anonymizer/extension`

**✅ Gotowe! Extension jest zainstalowany.**

---

### KROK 3: Sprawdź czy działa

1. Kliknij **ikonę extension** w Chrome (niebieska "P")
2. Sprawdź status:
   - **● ONLINE** (zielony) = Działa! ✅
   - **● OFFLINE** (szary) = Backend nie działa, wróć do KROKU 1

3. **Toggle "Auto-anonymize"** powinien być **włączony** (niebieski)

**✅ To wszystko! Extension działa automatycznie.**

---

## 🧪 Testuj!

### Test na ChatGPT:

1. Otwórz https://chat.openai.com
2. Wpisz w textarea:
   ```
   Cześć, jestem Jan Kowalski, PESEL 92010212345, email jan@example.com
   ```
3. **Poczekaj 500ms** (extension przetwarza w tle)
4. **Zobacz rezultat:**
   - Tekst zmieni się na: `"PESEL [PESEL], email [EMAIL]"`
   - Notyfikacja w prawym górnym rogu: **"2 dane zanonimizowane"**
   - Textarea mignie zielonym obramowaniem

**✅ Działa!**

---

## 💡 Jak to działa?

**Extension automatycznie:**
1. ✅ Łączy się z backendem (localhost:4222)
2. ✅ Pobiera token autoryzacyjny (w tle, nie musisz nic robić)
3. ✅ Monitoruje textarea w ChatGPT/Claude/Perplexity
4. ✅ Wysyła tekst do backendu
5. ✅ Zastępuje dane osobowe maskami: `[EMAIL]`, `[PESEL]`, `[TELEFON]`
6. ✅ Pokazuje notyfikację

**Ty tylko:**
- Uruchamiasz backend (KROK 1)
- Instalujesz extension (KROK 2)
- Korzystasz! (KROK 3)

---

## ❓ FAQ

### **Q: Muszę kopiować jakiś token?**
**A: NIE!** Extension automatycznie pobiera token z backendu. Nic nie musisz robić.

### **Q: Extension pokazuje "Offline"?**
**A:** Backend nie działa. Uruchom: `cd backend && source .venv/bin/activate && python app.py`

### **Q: Tekst nie jest anonimizowany?**
**A:** Sprawdź:
1. Extension jest włączony (toggle = ON)
2. Backend działa (status = ONLINE)
3. Czekasz 500ms po wpisaniu tekstu (debounce)

### **Q: Gdzie mogę zobaczyć co się dzieje?**
**A:** Otwórz dashboard: http://127.0.0.1:4222/dashboard
- Statystyki real-time
- Logi aktywności
- Test anonimizacji

### **Q: Czy muszę zawsze mieć terminal otwarty?**
**A:** Tak, backend musi działać w tle. Możesz uruchomić go w osobnym terminalu i zminimalizować.

**Opcjonalnie:** Stwórz alias w `.zshrc`:
```bash
alias presidio='cd /Users/gaca/presidio-local-anonymizer/backend && source .venv/bin/activate && python app.py'
```

Potem wystarczy: `presidio` 🚀

---

## 🎯 Podsumowanie

**Co musisz zrobić:**
1. Uruchomić backend (raz, zostaw w tle)
2. Załadować extension w Chrome (raz)
3. Gotowe! Wszystko działa automatycznie ✅

**Czego NIE musisz robić:**
- ❌ Kopiować tokenu
- ❌ Wklejać czegokolwiek
- ❌ Konfigurować ręcznie
- ❌ Nic!

**Po prostu działa!** 🎉
