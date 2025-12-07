# Dane Bez Twarzy - Dokumentacja Techniczna

## Architektura projektu

### Struktura katalogów

```
DaneBezTwarzy/
├── src/dane_bez_twarzy/        # Kod źródłowy biblioteki
│   ├── core/                    # Podstawowe komponenty
│   │   ├── anonymizer.py        # Główna klasa anonimizacji
│   │   ├── detector.py          # Wykrywanie encji
│   │   └── config.py            # Konfiguracja
│   ├── detectors/               # Detektory encji
│   │   ├── regex_detector.py    # Detekcja przez regex
│   │   ├── nlp_detector.py      # Detekcja przez NLP
│   │   └── polish_detector.py   # Polskie wzorce
│   ├── strategies/              # Strategie anonimizacji
│   │   └── __init__.py          # Wszystkie strategie
│   ├── processors/              # Procesory formatów plików
│   │   └── __init__.py          # Procesory dla txt, docx, xlsx, pdf
│   ├── utils/                   # Narzędzia pomocnicze
│   │   ├── patterns.py          # Wzorce regex
│   │   └── logger.py            # Logowanie
│   └── cli.py                   # Interface wiersza poleceń
├── tests/                       # Testy jednostkowe
├── examples/                    # Przykłady użycia
├── pyproject.toml              # Konfiguracja projektu
└── README.md                   # Dokumentacja użytkownika
```

## Główne komponenty

### 1. Anonymizer (core/anonymizer.py)
Główna klasa do anonimizacji danych. Koordynuje pracę detektorów i strategii.

**Kluczowe metody:**
- `anonymize_text(text)` - anonimizuje tekst
- `anonymize_file(input_path, output_path)` - anonimizuje plik
- `anonymize_directory(input_dir, output_dir)` - anonimizuje katalog
- `detect_entities(text)` - wykrywa encje bez anonimizacji
- `generate_report(text)` - generuje raport z analizy

### 2. EntityDetector (core/detector.py)
Wykrywa dane osobowe w tekście używając wielu metod:
- Wyrażenia regularne (szybkie, deterministyczne)
- NLP/NER przez spaCy (kontekstowe)
- Specjalistyczne detektory (np. dla polskich danych)

**Reprezentacja encji:**
```python
@dataclass
class Entity:
    text: str          # Wykryty tekst
    type: EntityType   # Typ encji (PERSON, EMAIL, itp.)
    start: int         # Pozycja początkowa
    end: int           # Pozycja końcowa
    confidence: float  # Pewność wykrycia (0-1)
    metadata: dict     # Dodatkowe informacje
```

### 3. AnonymizationConfig (core/config.py)
Konfiguracja procesu anonimizacji.

**Kluczowe parametry:**
- `language` - język dokumentu (domyślnie "pl")
- `method` - metoda anonimizacji (mask, pseudonymize, hash, itp.)
- `entities` - typy encji do anonimizacji
- `mask_char` - znak maskujący
- `seed` - seed dla pseudonimizacji
- `custom_patterns` - własne wzorce regex

### 4. Strategie anonimizacji (strategies/)

Wszystkie strategie dziedziczą po `AnonymizationStrategy`:

- **MaskStrategy** - zamienia znaki na maskę (****)
- **PseudonymizeStrategy** - tworzy konsystentne pseudonimy ([PERSON_1])
- **HashStrategy** - nieodwracalne haszowanie
- **RedactStrategy** - całkowite usunięcie ([USUNIĘTO])
- **GeneralizeStrategy** - zamiana na ogólne kategorie ([TELEFON])
- **EncryptStrategy** - odwracalne szyfrowanie

### 5. Procesory plików (processors/)

Każdy processor obsługuje inny format:
- **TextProcessor** - pliki .txt
- **DocxProcessor** - pliki .docx (Word)
- **ExcelProcessor** - pliki .xlsx, .csv
- **PDFProcessor** - pliki .pdf

## Rozpoznawane typy danych

### Dane polskie
- **PESEL** - z walidacją checksumy
- **NIP** - z walidacją checksumy
- **REGON** - 9 lub 14 cyfr
- **Dowód osobisty** - format ABC123456
- **Paszport** - format AB1234567
- **Numer rejestracyjny** - tablice pojazdu

### Dane międzynarodowe
- **Email** - standardowy format
- **Telefon** - polski format (+48...)
- **URL** - adresy internetowe
- **IP** - adresy IPv4
- **Karta kredytowa** - z algorytmem Luhna
- **Konto bankowe** - polski format (26 cyfr)

### Dane personalne
- **Imiona i nazwiska** - przez NLP
- **Organizacje** - przez NLP
- **Lokalizacje** - przez NLP i wzorce polskich adresów

## Zależności projektu

### Podstawowe zależności
```toml
spacy>=3.7.0              # NLP/NER
regex>=2023.12.0          # Wyrażenia regularne
cryptography>=41.0.0      # Kryptografia
pandas>=2.1.0             # Przetwarzanie danych
openpyxl>=3.1.0          # Excel
python-docx>=1.1.0       # Word
PyPDF2>=3.0.0            # PDF
langdetect>=1.0.9        # Wykrywanie języka
pydantic>=2.5.0          # Walidacja
tqdm>=4.66.0             # Paski postępu
colorlog>=6.8.0          # Kolorowe logi
```

### Opcjonalne zależności

**OCR (rozpoznawanie tekstu z obrazów):**
```toml
pytesseract>=0.3.10
Pillow>=10.1.0
pdf2image>=1.16.3
```

**Zaawansowane NLP:**
```toml
transformers>=4.36.0
torch>=2.1.0
```

**Deweloperskie:**
```toml
pytest>=7.4.0
pytest-cov>=4.1.0
black>=23.12.0
isort>=5.13.0
flake8>=7.0.0
mypy>=1.8.0
```

## Potencjalne rozszerzenia

### 1. Dodatkowe detektory
- Detektor twarzy w obrazach (OpenCV/dlib)
- Detektor głosów w audio
- Rozpoznawanie pisma ręcznego
- Detektor metadanych (EXIF)

### 2. Dodatkowe formaty
- RTF, ODT
- HTML, Markdown
- JSON, XML (głęboka anonimizacja)
- Bazy danych (SQL)
- Obrazy (OCR + detekcja twarzy)

### 3. Zaawansowane funkcje
- Differential privacy
- K-anonymity
- L-diversity
- Audit trail (ślad zmian)
- Backup i odzyskiwanie
- API REST/GraphQL
- GUI (Tkinter/PyQt)

### 4. Integracje
- Apache Spark (big data)
- Apache Kafka (streaming)
- Docker (konteneryzacja)
- Cloud (AWS, Azure, GCP)

### 5. Narzędzia
- Pre-commit hooks
- CI/CD (GitHub Actions)
- Dokumentacja (Sphinx/MkDocs)
- Benchmarking
- Monitoring i metryki

## Narzędzia do rozważenia

### NLP i ML
- **spaCy** ✓ (obecnie używane) - NER, przetwarzanie języka
- **transformers** (opcjonalne) - modele BERT, GPT
- **flair** - sequencje tagowania
- **stanza** - wielojęzyczne NLP

### Wykrywanie wzorców
- **presidio** (Microsoft) - framework do wykrywania PII
- **scrubadub** - czyszczenie danych
- **commonregex** - predefiniowane wzorce

### OCR
- **tesseract/pytesseract** ✓ (opcjonalne)
- **easyocr** - deep learning OCR
- **paddle-ocr** - wielojęzyczny OCR

### Przetwarzanie obrazów
- **opencv-python** - detekcja twarzy
- **face_recognition** - rozpoznawanie twarzy
- **Pillow** ✓ (opcjonalne) - manipulacja obrazami

### Formaty plików
- **pandoc** - konwersje formatów
- **textract** - ekstrakcja tekstu z wielu formatów
- **pdfplumber** - zaawansowane przetwarzanie PDF
- **camelot** - ekstrakcja tabel z PDF

### Kryptografia
- **cryptography** ✓ - szyfrowanie
- **hashlib** (stdlib) - haszowanie
- **secrets** (stdlib) - bezpieczne generowanie

### GUI
- **streamlit** - szybkie web UI
- **gradio** - interfejs ML
- **tkinter** - desktop GUI
- **PyQt5/PySide6** - zaawansowany GUI

### Testing
- **pytest** ✓
- **hypothesis** - property-based testing
- **faker** - generowanie testowych danych

## Wydajność i optymalizacja

### Aktualne podejście
- Lazy loading detektorów (spaCy ładowany tylko gdy potrzebny)
- Przetwarzanie strumieniowe dla dużych plików
- Deduplikacja encji

### Możliwe ulepszenia
- Równoległe przetwarzanie (multiprocessing)
- Caching wyników NLP
- Batching dla wielu plików
- GPU dla modeli ML
- Kompresja danych pośrednich

## Bezpieczeństwo

### Aktualne zabezpieczenia
- Walidacja PESEL, NIP, REGON, kart kredytowych
- Bezpieczne haszowanie (salt, seed)
- Szyfrowanie z cryptography

### Do rozważenia
- Bezpieczne usuwanie plików tymczasowych
- Audyt i logowanie operacji
- Kontrola dostępu
- Szyfrowanie w spoczynku i w tranzycie
- Compliance z RODO/GDPR

## Licencja
MIT License - open source, można używać komercyjnie
