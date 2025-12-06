# Katalog testów

## Struktura

### Skrypty testowe i narzędziowe:

- **`test_config.py`** - Testy jednostkowe konfiguracji (pytest)
- **`test_nlp_detection.py`** - Test wykrywania NLP dla polskich imion/nazwisk
- **`test_spacy_direct.py`** - Bezpośredni test modelu spaCy `pl_core_news_lg`
- **`test_quick.py`** - Szybki test podstawowej funkcjonalności
- **`analyze_orig.py`** - Analiza zawartości pliku orig.txt (statystyki placeholderów)
- **`create_sample.py`** - Generowanie przykładowych plików testowych

### Dane testowe (`test_data/`):

- **`test_sample.txt`** - Przykładowy tekst z placeholderami do testów
- **`test_input.txt`** - Plik wejściowy z danymi osobowymi
- **`test_input_anonimizowany.txt`** - Wynik anonimizacji
- **`test_data.txt`** - Dane testowe
- **`test_data_anonimizowany.txt`** - Wynik anonimizacji
- **`orig.txt`** - Kopia pliku z placeholderami
- **`output.txt`** - Wyjście z testów
- **`test_report.json`** - Raport z wykrytych encji (JSON)

## Uruchomienie testów

### Testy jednostkowe (pytest):
```bash
pytest
pytest --cov=dane_bez_twarzy --cov-report=html
```

### Testy manualne:
```bash
# Test NLP
python tests/test_nlp_detection.py

# Test spaCy
python tests/test_spacy_direct.py

# Szybki test
python tests/test_quick.py

# Analiza placeholderów
python tests/analyze_orig.py

# Generowanie przykładów
python tests/create_sample.py
```

## Wymagania

- Python 3.12+
- Zainstalowana biblioteka w trybie deweloperskim: `pip install -e .`
- Dla testów NLP: `pip install spacy` + model `pl_core_news_lg`
