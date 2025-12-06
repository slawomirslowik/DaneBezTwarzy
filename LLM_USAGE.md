# Instrukcja użycia detektora LLM (PLLUM)

## Instalacja

1. Zainstaluj bibliotekę z obsługą LLM:
```bash
pip install -e ".[llm]"
```

Lub zainstaluj zależności ręcznie:
```bash
pip install langchain-openai langchain
```

## Podstawowe użycie

### 1. Prosty przykład z detektorem LLM

```python
from dane_bez_twarzy.core.config import AnonymizationConfig, EntityType
from dane_bez_twarzy.core.anonymizer import Anonymizer

# Tekst do anonimizacji
text = """
Jan Kowalski, PESEL: 92101012345
Email: jan.kowalski@example.com
Telefon: +48 123 456 789
"""

# Konfiguracja
config = AnonymizationConfig(
    entities=[EntityType.PERSON, EntityType.EMAIL, EntityType.PHONE, EntityType.PESEL],
    method="mask",
    language="pl"
)

# Anonimizacja z użyciem LLM
anonymizer = Anonymizer(
    config,
    use_llm=True,
    llm_api_key="c670f40b37e0495c845c63b1e548d95a",
    llm_base_url="https://apim-pllum-tst-pcn.azure-api.net/vllm/v1",
    llm_model_name="CYFRAGOVPL/pllum-12b-nc-chat-250715"
)

result = anonymizer.anonymize_text(text)
print(result.anonymized_text)
```

### 2. Wykrywanie encji bez anonimizacji

```python
from dane_bez_twarzy.core.detector import EntityDetector
from dane_bez_twarzy.core.config import AnonymizationConfig, EntityType

text = "Jan Kowalski mieszka w Warszawie, tel: 123-456-789"

config = AnonymizationConfig(
    entities=[EntityType.PERSON, EntityType.PHONE, EntityType.ADDRESS]
)

# Tylko detekcja z LLM
detector = EntityDetector(
    config,
    use_llm=True,
    llm_api_key="twój_klucz_api"
)

entities = detector.detect(text)

for entity in entities:
    print(f"{entity.type.value}: '{entity.text}' (pewność: {entity.confidence:.2f})")
```

### 3. Kombinacja detektorów (regex + LLM)

```python
from dane_bez_twarzy.core.anonymizer import Anonymizer
from dane_bez_twarzy.core.config import AnonymizationConfig, EntityType

config = AnonymizationConfig(
    entities=[
        EntityType.PERSON,
        EntityType.EMAIL,
        EntityType.PHONE,
        EntityType.PESEL,
        EntityType.ADDRESS
    ],
    use_nlp=False  # Wyłączamy spaCy
)

# Użyj zarówno regex (szybki) jak i LLM (dokładny)
anonymizer = Anonymizer(
    config,
    use_llm=True,
    llm_api_key="twój_klucz_api"
)

# Regex wykryje PESEL, email, telefon (wzorce)
# LLM wykryje imiona, nazwiska, adresy (kontekst)
result = anonymizer.anonymize_text(text)
```

## Zaawansowane użycie

### Własne parametry LLM

```python
from dane_bez_twarzy.detectors.llm_detector import LLMDetector
from dane_bez_twarzy.core.config import AnonymizationConfig

config = AnonymizationConfig()

detector = LLMDetector(
    config,
    api_key="twój_klucz",
    base_url="https://twój-endpoint.com/v1",
    model_name="nazwa_modelu"
)

entities = detector.detect(text)
```

### Zmienne środowiskowe

Możesz również ustawić klucz API jako zmienną środowiskową:

```bash
# Linux/Mac
export PLLUM_API_KEY="c670f40b37e0495c845c63b1e548d95a"
export PLLUM_BASE_URL="https://apim-pllum-tst-pcn.azure-api.net/vllm/v1"

# Windows PowerShell
$env:PLLUM_API_KEY="c670f40b37e0495c845c63b1e548d95a"
$env:PLLUM_BASE_URL="https://apim-pllum-tst-pcn.azure-api.net/vllm/v1"
```

Następnie w kodzie:

```python
import os

anonymizer = Anonymizer(
    config,
    use_llm=True,
    llm_api_key=os.getenv("PLLUM_API_KEY"),
    llm_base_url=os.getenv("PLLUM_BASE_URL")
)
```

## Uruchomienie przykładu

```bash
python examples/llm_usage.py
```

## Typy wykrywanych encji przez LLM

LLM może wykrywać:
- **PERSON** - imiona i nazwiska
- **EMAIL** - adresy email
- **PHONE** - numery telefonu
- **PESEL** - numery PESEL
- **NIP** - numery NIP
- **REGON** - numery REGON
- **ADDRESS** - adresy (ulice, miasta, kody pocztowe)
- **CREDIT_CARD** - numery kart kredytowych
- **IBAN** - numery kont bankowych
- **ID_CARD** - numery dowodów osobistych
- **PASSPORT** - numery paszportów
- **ORGANIZATION** - nazwy firm i organizacji
- **DATE** - daty urodzenia i inne wrażliwe daty

## Zalety detektora LLM

✅ **Wykrywanie kontekstowe** - rozumie kontekst i semantykę
✅ **Elastyczność** - wykrywa nietypowe formaty
✅ **Wysoka dokładność** - model językowy jest świadomy kontekstu
✅ **Wsparcie dla języka polskiego** - PLLUM jest trenowany na polskich danych

## Ograniczenia

⚠️ **Koszt** - zapytania do API LLM mogą być kosztowne
⚠️ **Szybkość** - wolniejsze niż regex
⚠️ **Wymaga połączenia** - potrzebny dostęp do API
⚠️ **Zależność od modelu** - wyniki zależą od jakości modelu

## Najlepsze praktyki

1. **Hybrydowe podejście**: Użyj regex dla prostych wzorców (PESEL, NIP) i LLM dla złożonych (imiona, adresy)
2. **Cache**: Cachuj wyniki dla tych samych tekstów
3. **Batch processing**: Przetwarzaj wiele tekstów naraz
4. **Fallback**: Miej plan B na wypadek niedostępności API

## Troubleshooting

### Błąd: "Module 'langchain_openai' not found"

```bash
pip install langchain-openai
```

### Błąd: "API key invalid"

Sprawdź czy klucz API jest poprawny i aktywny.

### Błąd: "Connection timeout"

Sprawdź połączenie sieciowe i dostępność API.

## Porównanie detektorów

| Detektor | Szybkość | Dokładność | Koszt | Offline |
|----------|----------|------------|-------|---------|
| Regex    | ⚡⚡⚡    | ⭐⭐       | 💰    | ✅      |
| spaCy NLP| ⚡⚡      | ⭐⭐⭐     | 💰    | ✅      |
| LLM      | ⚡        | ⭐⭐⭐⭐   | 💰💰💰 | ❌      |

## Kontakt i wsparcie

W razie problemów, utwórz issue na GitHubie lub skontaktuj się z zespołem.
