# Instrukcja instalacji i uruchomienia

## Wymagania wstępne
- Python 3.9 lub nowszy
- pip

## Instalacja w trybie deweloperskim

1. Sklonuj repozytorium (lub przejdź do katalogu projektu):
```bash
cd DaneBezTwarzy
```

2. Utwórz środowisko wirtualne:
```bash
python -m venv venv
```

3. Aktywuj środowisko wirtualne:
```bash
# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

4. Zainstaluj bibliotekę w trybie edytowalnym:
```bash
pip install -e .
```

5. Zainstaluj model spaCy dla języka polskiego:
```bash
python -m spacy download pl_core_news_lg
```

**Uwaga:** Jeśli wystąpi błąd związany z pydantic podczas instalacji modelu spaCy, użyj alternatywnej metody:
```bash
pip install https://github.com/explosion/spacy-models/releases/download/pl_core_news_lg-3.7.0/pl_core_news_lg-3.7.0-py3-none-any.whl
```

6. Zainstaluj zależności deweloperskie (opcjonalnie):
```bash
pip install -e ".[dev]"
```

## Opcjonalne instalacje

### OCR (rozpoznawanie tekstu z obrazów)
```bash
pip install -e ".[ocr]"
```

### Zaawansowane NLP
```bash
pip install -e ".[advanced-nlp]"
```

## Uruchomienie przykładów

```bash
python examples/basic_usage.py
```

## Uruchomienie testów

```bash
pytest
pytest --cov=dane_bez_twarzy --cov-report=html
```

## Użycie CLI

```bash
# Anonimizacja pojedynczego pliku
dane-bez-twarzy anonymize input.txt -o output.txt --method mask

# Anonimizacja katalogu
dane-bez-twarzy anonymize-dir ./input_dir -o ./output_dir --recursive

# Wykrywanie encji
dane-bez-twarzy detect input.txt --report report.json
```
