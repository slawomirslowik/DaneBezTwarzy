# Instrukcja instalacji i uruchomienia

## Wymagania wstępne
- Python 3.12 
- pip

## Instalacja w trybie deweloperskim

1. Sklonuj repozytorium (lub przejdź do katalogu projektu):
```bash
cd DaneBezTwarzy
```

2. - Utwórz środowisko wirtualne:
```bash
python -m venv venv
```

- Aktywuj środowisko wirtualne:
```bash
# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```
Lub użyj narzędzia virtualenvwrapper-win: 

```bash
# Windows (w trybie admina)
pip install virtualenvwrapper-win
```

Utwórz nowe środowisko:
```bash
mkvirtualenv <nazwa>
```

I aktywuj:

```bash
workon <nazwa>
```

4. Zainstaluj bibliotekę w trybie edytowalnym:
```bash
pip install -e .
```

**Biblioteka zadziała bez spaCy - używając tylko detektorów regex (PESEL, NIP, email, telefon, itp.)**

5. (Opcjonalnie) Zainstaluj spaCy dla zaawansowanego NLP:

**UWAGA:** Na Windows spaCy wymaga Visual C++ Build Tools!

**Metoda A - Precompilowane pakiety (ZALECANE dla Windows):**
```bash
# Zainstaluj spaCy z gotowymi pakietami
pip install spacy==3.7.2 --only-binary :all:

# Zainstaluj model
pip install https://github.com/explosion/spacy-models/releases/download/pl_core_news_lg-3.7.0/pl_core_news_lg-3.7.0-py3-none-any.whl
```

**Metoda B - Kompilacja (wymaga Visual C++ Build Tools):**
```bash
# Najpierw zainstaluj Visual C++ Build Tools z:
# https://visualstudio.microsoft.com/visual-cpp-build-tools/

pip install -e ".[nlp]"
python -m spacy download pl_core_news_lg
```

**Metoda C - Użycie bez NLP:**
W kodzie ustaw `use_nlp=False` - biblioteka będzie działać z detektorami regex:
```python
config = AnonymizationConfig(use_nlp=False)
```

6. Zainstaluj zależności deweloperskie (opcjonalnie):
```bash
pip install -e ".[dev]"
```

## Opcjonalne instalacje

### NLP z spaCy (wykrywanie imion/nazwisk)
```bash
pip install -e ".[nlp]"
```

### OCR (rozpoznawanie tekstu z obrazów)
```bash
pip install -e ".[ocr]"
```

### Zaawansowane NLP (Transformers)
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
# Anonimizacja pojedynczego pliku (domyślnie BEZ NLP)
dane-bez-twarzy anonymize input.txt -o output.txt --method mask

# Anonimizacja Z NLP (wykrywanie imion/nazwisk przez spaCy)
dane-bez-twarzy anonymize input.txt -o output.txt --use-nlp

# Anonimizacja katalogu (rekurencyjnie)
dane-bez-twarzy anonymize-dir ./input_dir -o ./output_dir --recursive

# Anonimizacja katalogu Z NLP
dane-bez-twarzy anonymize-dir ./input_dir -o ./output_dir --use-nlp --recursive

# Wykrywanie encji (raport bez anonimizacji)
dane-bez-twarzy detect input.txt --report report.json

# Wykrywanie Z NLP
dane-bez-twarzy detect input.txt --report report.json --use-nlp

# Tryb szczegółowy (verbose - pokazuje debug)
dane-bez-twarzy anonymize input.txt -o output.txt -v
```

## Detektory

Biblioteka używa **4 detektorów** (3 zawsze aktywne + 1 opcjonalny):

### Zawsze aktywne (szybkie, bez dodatkowej instalacji):
1. **PlaceholderDetector** - wykrywa `[name]`, `[email]`, `[phone]`, `[address]` itp.
2. **RegexDetector** - wykrywa PESEL, NIP, REGON, email, telefon, konto bankowe
3. **PolishDetector** - wykrywa polskie wzorce (kody pocztowe, adresy, numery dokumentów)

### Opcjonalny (wymaga spaCy i flagi `--use-nlp`):
4. **NLPDetector** - wykrywa imiona, nazwiska, organizacje przez Named Entity Recognition

**Domyślnie**: Szybkie wykrywanie bez NLP (Placeholdery + Regex + Polskie wzorce)  
**Z flagą `--use-nlp`**: Wszystkie 4 detektory (wolniejsze, ale dokładniejsze dla imion/nazwisk)
```
