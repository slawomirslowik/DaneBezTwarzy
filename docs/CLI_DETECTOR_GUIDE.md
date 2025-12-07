# Szybki przewodnik: Wybór detektora (NLP vs LLM)

## 🎯 Który detektor wybrać?

### Tabela porównawcza

| Cecha | Regex | NLP (spaCy) | LLM (PLLUM) |
|-------|-------|-------------|-------------|
| **Szybkość** | ⚡⚡⚡ Bardzo szybki | ⚡⚡ Średni | ⚡ Wolny |
| **Dokładność** | ⭐⭐ Podstawowa | ⭐⭐⭐ Dobra | ⭐⭐⭐⭐ Bardzo dobra |
| **Offline** | ✅ Tak | ✅ Tak | ❌ Nie (API) |
| **Koszt** | 💰 Darmowy | 💰 Darmowy | 💰💰💰 Płatne API |
| **Instalacja** | ✅ Automatyczna | ⚠️ Wymaga modelu | ✅ Prosta + klucz API |
| **Kontekst** | ❌ Bez kontekstu | ✅ Rozumie kontekst | ✅✅ Świetnie rozumie |

## 📋 Rekomendacje

### 1. **Regex (domyślnie)** - Dla większości przypadków
```bash
dane-bez-twarzy anonymize input.txt -o output.txt
```
**Wykrywa:** PESEL, NIP, email, telefon, IBAN, karty kredytowe
**Używaj gdy:** Masz strukturyzowane dane, chcesz szybkości, pracujesz offline

### 2. **Regex + NLP** - Dla tekstów z imionami/nazwiskami
```bash
dane-bez-twarzy anonymize input.txt -o output.txt --use-nlp
```
**Dodatkowo wykrywa:** Imiona, nazwiska, nazwy organizacji
**Używaj gdy:** Przetwarzasz teksty opisowe, raporty, korespondencję

### 3. **Regex + LLM** - Dla maksymalnej dokładności
```bash
dane-bez-twarzy anonymize input.txt -o output.txt \
  --use-llm \
  --llm-api-key "twoj_klucz"
```
**Dodatkowo wykrywa:** Kontekstowe adresy, nietypowe formaty, ukryte dane
**Używaj gdy:** Dokładność > koszt, masz trudne przypadki, potrzebujesz pewności

### 4. **Wszystkie (Regex + NLP + LLM)** - Maksymalna ochrona
```bash
dane-bez-twarzy anonymize input.txt -o output.txt \
  --use-nlp \
  --use-llm \
  --llm-api-key "twoj_klucz"
```
**Używaj gdy:** Dane są krytyczne, możesz pozwolić na koszt i czas

## 🔧 Parametry CLI

### Opcje dla NLP
```bash
--use-nlp          # Włącz detektor NLP (spaCy)
--no-nlp           # Jawnie wyłącz NLP (przydatne z config.json)
```

### Opcje dla LLM
```bash
--use-llm          # Włącz detektor LLM
--llm-api-key      # Klucz API (wymagany dla LLM)
--llm-base-url     # URL API (opcjonalny, ma domyślny)
--llm-model        # Nazwa modelu (opcjonalny, ma domyślny)
```

## 📝 Przykłady użycia

### Przypadek 1: Szybkie przetwarzanie dużej liczby plików
```bash
# Tylko Regex - najszybsze
dane-bez-twarzy anonymize-dir ./dane -o ./output --recursive
```

### Przypadek 2: CV i dokumenty HR
```bash
# Regex + NLP - wykryje imiona/nazwiska
dane-bez-twarzy anonymize cv.docx -o cv_anon.docx --use-nlp
```

### Przypadek 3: Dokumentacja medyczna (krytyczna)
```bash
# Wszystkie detektory - maksymalna ochrona
dane-bez-twarzy anonymize pacjent.txt -o pacjent_anon.txt \
  --use-nlp \
  --use-llm \
  --llm-api-key "$PLLUM_API_KEY"
```

### Przypadek 4: Testy i rozwój
```bash
# Tylko wykrywanie, bez anonimizacji
dane-bez-twarzy detect test.txt --use-llm --llm-api-key "klucz" --report report.json
```

### Przypadek 5: Produkcja z logami
```bash
# Z verbose dla monitorowania
dane-bez-twarzy anonymize data.txt -o output.txt \
  --use-llm \
  --llm-api-key "klucz" \
  -v
```

## 🔐 Bezpieczeństwo klucza API

### Metoda 1: Zmienna środowiskowa (zalecana)
```bash
# Windows PowerShell
$env:PLLUM_API_KEY="c670f40b37e0495c845c63b1e548d95a"
dane-bez-twarzy anonymize input.txt -o output.txt --use-llm --llm-api-key $env:PLLUM_API_KEY

# Linux/Mac
export PLLUM_API_KEY="c670f40b37e0495c845c63b1e548d95a"
dane-bez-twarzy anonymize input.txt -o output.txt --use-llm --llm-api-key "$PLLUM_API_KEY"
```

### Metoda 2: Plik konfiguracyjny (dla powtarzalnego użycia)
```json
# config.json
{
  "method": "mask",
  "use_nlp": false,
  "entities": ["PERSON", "EMAIL", "PHONE", "ADDRESS"]
}
```

```bash
dane-bez-twarzy anonymize input.txt -o output.txt \
  -c config.json \
  --use-llm \
  --llm-api-key "klucz"
```

## ⚡ Optymalizacja wydajności

### Dla pojedynczych plików
```bash
# LLM - najdokładniejsze
dane-bez-twarzy anonymize vip_document.txt -o output.txt \
  --use-llm --llm-api-key "klucz"
```

### Dla batch processing
```bash
# Tylko Regex lub Regex+NLP - szybsze
dane-bez-twarzy anonymize-dir ./bulk_data -o ./output \
  --use-nlp \
  --recursive
```

## 🎓 Podsumowanie

**Wybieraj detektor według potrzeb:**

1. **Prostota + Szybkość** → Tylko Regex (domyślnie)
2. **Imiona/Nazwiska** → Regex + NLP (`--use-nlp`)
3. **Maksymalna dokładność** → Regex + LLM (`--use-llm`)
4. **Krytyczne dane** → Wszystkie (`--use-nlp --use-llm`)

**Pamiętaj:**
- LLM wymaga klucza API i połączenia internetowego
- NLP wymaga zainstalowania modelu spaCy
- Regex działa zawsze, bez dodatkowej konfiguracji
