# Dane Bez Twarzy

**Biblioteka do anonimizacji danych osobowych w plikach**

## 📋 Opis

`dane-bez-twarzy` to kompleksowa biblioteka Python do automatycznej anonimizacji danych osobowych (PII - Personally Identifiable Information) w różnych formatach plików. Biblioteka pomaga w zapewnieniu zgodności z RODO/GDPR poprzez wykrywanie i anonimizację wrażliwych danych.

## ✨ Funkcjonalności

### Wykrywanie i anonimizacja:
- **Dane osobowe**: imiona, nazwiska, PESEL, NIP, REGON
- **Dane kontaktowe**: adresy email, numery telefonu, adresy pocztowe
- **Dane finansowe**: numery kont bankowych, kart płatniczych
- **Dane lokalizacyjne**: adresy, współrzędne GPS
- **Dane identyfikacyjne**: numery dokumentów, numery rejestracyjne
- **Daty urodzenia i inne dane wrażliwe**
- **Placeholdery**: `[name]`, `[email]`, `[phone]`, `[address]` itp.

### Detektory (automatyczne):
Biblioteka używa **czterech detektorów** działających równolegle:

1. **PlaceholderDetector** ✅ (zawsze aktywny)
   - Wykrywa placeholdery w notacji `[name]`, `[surname]`, `[email]`, `[phone]`, `[pesel]`, `[city]` itp.
   - Obsługuje 30+ typów placeholderów używanych w templatech i plikach treningowych
   - Pewność: 1.0 (najwyższa)

2. **RegexDetector** ✅ (zawsze aktywny)
   - Wykrywa dane przez wyrażenia regularne: PESEL, NIP, REGON, email, telefon, konto bankowe
   - Szybki i deterministyczny
   - Pewność: 0.8-0.95

3. **PolishDetector** ✅ (aktywny gdy `language="pl"`)
   - Wykrywa polskie wzorce: adresy, kody pocztowe, numery dokumentów
   - Pewność: 0.7-0.9

4. **NLPDetector** ⚠️ (wymaga `--use-nlp` lub `use_nlp=True`)
   - Wykrywa imiona/nazwiska/organizacje przez spaCy NER (Named Entity Recognition)
   - Model: `pl_core_news_lg` dla języka polskiego
   - Wolniejszy, ale wykrywa kontekstowe dane osobowe
   - Pewność: 0.6-0.95

**Domyślnie**: Placeholdery + Regex + Polskie wzorce (szybkie, bez NLP)  
**Z NLP**: Wszystkie 4 detektory (dokładniejsze, wolniejsze)

### Obsługiwane formaty:
- 📄 Dokumenty tekstowe (TXT, DOCX, ODT)
- 📊 Arkusze kalkulacyjne (XLSX, CSV)
- 📑 Pliki PDF
- 🗂️ JSON, XML
- 🖼️ Obrazy z tekstem (OCR) - opcjonalnie

### Metody anonimizacji:
- **Maskowanie**: zamiana na `***` lub `[UKRYTO]`
- **Pseudonimizacja**: zamiana na konsystentne pseudonimy
- **Generalizacja**: zamiana na ogólniejsze wartości
- **Haszowanie**: nieodwracalne haszowanie wartości
- **Usuwanie**: całkowite usunięcie danych
- **Szyfrowanie**: szyfrowanie z możliwością odzyskania

## 🚀 Instalacja

```bash
pip install dane-bez-twarzy
```

### Instalacja z dodatkowymi funkcjami:

```bash
# Z obsługą OCR
pip install dane-bez-twarzy[ocr]

# Z zaawansowanym NLP
pip install dane-bez-twarzy[advanced-nlp]

# Z detektorem LLM (PLLUM)
pip install dane-bez-twarzy[llm]

# Dla deweloperów
pip install dane-bez-twarzy[dev]
```

### Instalacja modelu spaCy dla języka polskiego:

```bash
python -m spacy download pl_core_news_lg
```

## 📖 Szybki start

### Podstawowe użycie:

```python
from dane_bez_twarzy import Anonymizer, AnonymizationConfig

# Konfiguracja
config = AnonymizationConfig(
    language="pl",
    method="mask",
    mask_char="*",
    preserve_length=True
)

# Inicjalizacja
anonymizer = Anonymizer(config)

# Anonimizacja tekstu
text = "Jan Kowalski, PESEL: 90010112345, email: jan.kowalski@example.com"
result = anonymizer.anonymize_text(text)
print(result)
# Wynik: "*** ********, PESEL: ***********, email: *********************"

# Anonimizacja pliku
anonymizer.anonymize_file(
    input_path="dokument.docx",
    output_path="dokument_anonimizowany.docx"
)
```

### Zaawansowane użycie:

```python
from dane_bez_twarzy import Anonymizer, AnonymizationConfig, EntityType

# Precyzyjna konfiguracja
config = AnonymizationConfig(
    language="pl",
    entities=[
        EntityType.PERSON,
        EntityType.EMAIL,
        EntityType.PHONE,
        EntityType.PESEL,
        EntityType.BANK_ACCOUNT
    ],
    method="pseudonymize",
    seed=12345  # Dla powtarzalnych pseudonimów
)

anonymizer = Anonymizer(config)

# Batch processing
anonymizer.anonymize_directory(
    input_dir="./dane_wrażliwe",
    output_dir="./dane_anonimizowane",
    recursive=True,
    file_patterns=["*.docx", "*.xlsx", "*.pdf"]
)
```

### CLI (Command Line Interface):

```bash
# Pojedynczy plik (domyślnie bez NLP - szybkie, tylko regex)
dane-bez-twarzy anonymize input.docx -o output.docx --method mask

# Włącz NLP (wykrywanie imion/nazwisk przez spaCy)
dane-bez-twarzy anonymize input.txt -o output.txt --use-nlp

# Jawnie wyłącz NLP (przydatne gdy w config.json jest use_nlp=true)
dane-bez-twarzy anonymize input.txt -o output.txt --no-nlp

# Z różnymi metodami
dane-bez-twarzy anonymize input.txt -o output.txt --method pseudonymize
dane-bez-twarzy anonymize input.txt -o output.txt --method generalize

# Katalog (rekurencyjnie)
dane-bez-twarzy anonymize-dir ./input_dir -o ./output_dir --recursive

# Katalog z NLP
dane-bez-twarzy anonymize-dir ./input_dir -o ./output_dir --use-nlp --recursive

# Z plikiem konfiguracyjnym
dane-bez-twarzy anonymize input.xlsx -c config.json

# Z plikiem konfiguracyjnym + nadpisanie ustawienia NLP
dane-bez-twarzy anonymize input.xlsx -c config.json --no-nlp

# Analiza bez anonimizacji (raport z wykrytych danych)
dane-bez-twarzy detect input.txt --report report.json

# Użycie detektora LLM (PLLUM)
dane-bez-twarzy anonymize input.txt -o output.txt --use-llm --llm-api-key "twoj_klucz"

# LLM z pełnymi parametrami
dane-bez-twarzy anonymize input.txt -o output.txt \
  --use-llm \
  --llm-api-key "c670f40b37e0495c845c63b1e548d95a" \
  --llm-base-url "https://apim-pllum-tst-pcn.azure-api.net/vllm/v1" \
  --llm-model "CYFRAGOVPL/pllum-12b-nc-chat-250715"

# Kombinacja NLP + LLM (maksymalna dokładność)
dane-bez-twarzy anonymize input.txt -o output.txt --use-nlp --use-llm --llm-api-key "klucz"

# Detekcja z LLM
dane-bez-twarzy detect input.txt --use-llm --llm-api-key "klucz" --report report.json

# Tryb szczegółowy (verbose)
# Flaga -v włącza tryb DEBUG, wyświetlając szczegółowe informacje diagnostyczne:
# - Postęp wykrywania encji przez każdy detektor
# - Informacje o przetwarzaniu fragmentów tekstu (chunking) przez LLM
# - Szczegóły operacji na plikach i katalogach
# - Przydatne do debugowania i monitorowania procesu anonimizacji
dane-bez-twarzy anonymize input.txt -o output.txt -v


# Full opcja (anominizacja przy użyciu wszystkich mwetod/modeli w trybie verbose oraz wygenerowanie pełnego raportu"):
dane-bez-twarzy anonymize text1.txt -o text1-outputxxx.txt --method entity --use-nlp --use-llm --llm-api-key "c670f40b37e0495c845c63b1e548d95a" --add-report wynikixxx --report-format all -v
```

### Użycie z detektorem LLM (PLLUM):

```python
from dane_bez_twarzy import Anonymizer, AnonymizationConfig, EntityType

# Konfiguracja
config = AnonymizationConfig(
    entities=[EntityType.PERSON, EntityType.EMAIL, EntityType.ADDRESS],
    method="mask"
)

# Użycie detektora LLM dla większej dokładności
anonymizer = Anonymizer(
    config,
    use_llm=True,
    llm_api_key="twój_klucz_api",
    llm_base_url="https://apim-pllum-tst-pcn.azure-api.net/vllm/v1",
    llm_model_name="CYFRAGOVPL/pllum-12b-nc-chat-250715"
)

text = "Jan Kowalski mieszka przy ul. Kwiatowej 15 w Warszawie"
result = anonymizer.anonymize_text(text)
print(result.anonymized_text)
```

📚 **Więcej informacji o LLM**: Zobacz [LLM_USAGE.md](LLM_USAGE.md)

## ⚙️ Konfiguracja

### Plik konfiguracyjny (JSON):

```json
{
  "language": "pl",
  "method": "pseudonymize",
  "entities": ["PERSON", "EMAIL", "PHONE", "PESEL"],
  "preserve_structure": true,
  "mask_char": "*",
  "seed": 12345,
  "custom_patterns": {
    "custom_id": "\\b[A-Z]{2}\\d{6}\\b"
  }
}
```

## 🔧 Architektura

```
dane_bez_twarzy/
├── core/
│   ├── anonymizer.py       # Główna klasa anonimizacji
│   ├── detector.py          # Wykrywanie encji
│   └── config.py            # Konfiguracja
├── strategies/
│   ├── mask.py              # Maskowanie
│   ├── pseudonymize.py      # Pseudonimizacja
│   ├── hash.py              # Haszowanie
│   └── generalize.py        # Generalizacja
├── detectors/
│   ├── regex_detector.py    # Detekcja regex
│   ├── nlp_detector.py      # NLP/NER (spaCy)
│   ├── llm_detector.py      # LLM (PLLUM) - nowy!
│   └── polish_detector.py   # Polskie wzorce
├── processors/
│   ├── text_processor.py    # Teksty
│   ├── docx_processor.py    # DOCX
│   ├── pdf_processor.py     # PDF
│   ├── excel_processor.py   # Excel/CSV
│   └── image_processor.py   # OCR (opcjonalnie)
└── utils/
    ├── patterns.py          # Wzorce regex
    ├── validators.py        # Walidacja
    └── logger.py            # Logowanie
```

## 🧪 Testy

```bash
pytest
pytest --cov=dane_bez_twarzy --cov-report=html
```

## 📊 Przykładowe wzorce

Biblioteka rozpoznaje m.in.:

### Dane osobowe (Regex):
- **PESEL**: `90010112345`
- **NIP**: `123-456-78-90`, `1234567890`
- **REGON**: `123456789`, `12345678901234`
- **Telefon**: `+48 123 456 789`, `123-456-789`
- **Email**: `jan.kowalski@example.com`
- **Konto bankowe**: `12 3456 7890 1234 5678 9012 3456`
- **Dowód osobisty**: `ABC123456`

### Placeholdery (PlaceholderDetector):
- `[name]`, `[surname]` → `PERSON`
- `[email]` → `EMAIL`
- `[phone]` → `PHONE`
- `[address]` → `ADDRESS`
- `[city]` → `LOCATION`
- `[pesel]` → `PESEL`
- `[nip]` → `NIP`
- `[company]` → `ORGANIZATION`
- `[date]`, `[birth-date]` → `DATE`
- `[age]` → `AGE`
- `[sex]` → `SEX`
- `[password]`, `[secret]` → `SECRET`
- `[username]` → `USERNAME`
- `[job-title]` → `JOB_TITLE`

### Imiona/nazwiska (NLPDetector - wymaga `--use-nlp`):
- **Jan Kowalski**, **Anna Nowak**, **Piotr Wiśniewski**
- Wykrywane kontekstowo przez model spaCy `pl_core_news_lg`

## 📋 Logowanie

Biblioteka automatycznie loguje wszystkie operacje do:

### Konsola (stdout)
- Poziom: INFO (domyślnie) lub DEBUG (z flagą `-v`)
- Kolorowe komunikaty (jeśli `colorlog` jest zainstalowane)
- Format: `INFO     Wiadomość`

### Plik: `dane_bez_twarzy.log`
- Tworzony automatycznie w bieżącym katalogu
- Zawsze loguje wszystkie poziomy (DEBUG i wyżej)
- Format szczegółowy z timestampem, funkcją i numerem linii
- **Rotacja**: maksymalnie 5 plików × 10 MB każdy

**Przykład zawartości pliku logu:**
```
2025-12-06 15:30:45 - dane_bez_twarzy - INFO - anonymize_file:234 - Anonimizacja pliku: input.txt -> output.txt
2025-12-06 15:30:46 - dane_bez_twarzy - DEBUG - detect:89 - Znaleziono 15 encji typu PERSON
2025-12-06 15:30:47 - dane_bez_twarzy - INFO - anonymize_file:251 - Plik zanonimizowany: output.txt
```

**Pliki logów:**
```
dane_bez_twarzy.log       # Aktualny (do 10 MB)
dane_bez_twarzy.log.1     # Poprzedni
dane_bez_twarzy.log.2
dane_bez_twarzy.log.3
dane_bez_twarzy.log.4
dane_bez_twarzy.log.5     # Najstarszy
```

## 🤝 Wkład

Zapraszamy do współpracy! Zobacz [CONTRIBUTING.md](CONTRIBUTING.md) #TODO

## 📄 Licencja

MIT License - zobacz [LICENSE](LICENSE)

## ⚠️ Uwagi prawne

Ta biblioteka jest narzędziem pomocniczym. Użytkownik jest odpowiedzialny za:
- Weryfikację wyników anonimizacji
- Zgodność z lokalnymi przepisami (RODO/GDPR)
- Bezpieczne przechowywanie danych

## 📞 Kontakt

- Issues: https://github.com/yourusername/dane-bez-twarzy/issues
- Email: semantis@int.pl
