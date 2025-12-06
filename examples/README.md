# Przykłady użycia

Ten katalog zawiera przykłady użycia biblioteki `dane-bez-twarzy`.

## Dostępne przykłady

### 1. `basic_usage.py`
Podstawowe użycie biblioteki z detektorami regex i spaCy NLP.

```bash
python examples/basic_usage.py
```

Pokazuje:
- Anonimizację tekstu
- Wykrywanie różnych typów encji (PESEL, email, telefon, itp.)
- Różne metody anonimizacji (maskowanie, pseudonimizacja)

### 2. `llm_usage.py` ⭐ NOWY!
Użycie detektora LLM (PLLUM) do wykrywania danych wrażliwych.

```bash
# Najpierw zainstaluj zależności
pip install -e ".[llm]"

# Uruchom przykład
python examples/llm_usage.py
```

Pokazuje:
- Detekcję encji używając modelu językowego PLLUM
- Anonimizację z użyciem LLM
- Porównanie z innymi detektorami

**Uwaga:** Wymaga klucza API do PLLUM.

## Szybki test

Aby szybko przetestować bibliotekę bez instalacji spaCy czy LLM:

```python
from dane_bez_twarzy.core.config import AnonymizationConfig, EntityType
from dane_bez_twarzy.core.anonymizer import Anonymizer

# Prosty test z samym regex (nie wymaga dodatkowych bibliotek)
config = AnonymizationConfig(
    entities=[EntityType.EMAIL, EntityType.PHONE, EntityType.PESEL],
    use_nlp=False  # Wyłącz spaCy
)

anonymizer = Anonymizer(config)  # Bez use_llm=True

text = """
Kontakt: jan.kowalski@example.com
Telefon: +48 123 456 789
PESEL: 92101012345
"""

result = anonymizer.anonymize_text(text)
print(result.anonymized_text)
```

## Uwagi

- Przykłady **bez NLP** działają od razu po instalacji podstawowej
- Przykłady **z NLP** wymagają: `pip install -e ".[nlp]"` + model spaCy
- Przykłady **z LLM** wymagają: `pip install -e ".[llm]"` + klucz API

## Dokumentacja

- [README.md](../README.md) - Główna dokumentacja
- [INSTALL.md](../INSTALL.md) - Instrukcje instalacji
- [LLM_USAGE.md](../LLM_USAGE.md) - Szczegóły użycia detektora LLM
- [TECHNICAL.md](../TECHNICAL.md) - Dokumentacja techniczna
