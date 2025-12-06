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
# Pojedynczy plik
dane-bez-twarzy anonymize input.docx -o output.docx --method mask

# Katalog
dane-bez-twarzy anonymize-dir ./input_dir -o ./output_dir --recursive

# Z konfiguracją
dane-bez-twarzy anonymize input.xlsx -c config.json

# Analiza bez anonimizacji
dane-bez-twarzy detect input.txt --report report.json
```

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
│   ├── nlp_detector.py      # NLP/NER
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
- **PESEL**: `90010112345`
- **NIP**: `123-456-78-90`, `1234567890`
- **REGON**: `123456789`, `12345678901234`
- **Telefon**: `+48 123 456 789`, `123-456-789`
- **Email**: `jan.kowalski@example.com`
- **Konto bankowe**: `12 3456 7890 1234 5678 9012 3456`
- **Dowód osobisty**: `ABC123456`

## 🤝 Wkład

Zapraszamy do współpracy! Zobacz [CONTRIBUTING.md](CONTRIBUTING.md)

## 📄 Licencja

MIT License - zobacz [LICENSE](LICENSE)

## ⚠️ Uwagi prawne

Ta biblioteka jest narzędziem pomocniczym. Użytkownik jest odpowiedzialny za:
- Weryfikację wyników anonimizacji
- Zgodność z lokalnymi przepisami (RODO/GDPR)
- Bezpieczne przechowywanie danych

## 📞 Kontakt

- Issues: https://github.com/yourusername/dane-bez-twarzy/issues
- Email: your.email@example.com
