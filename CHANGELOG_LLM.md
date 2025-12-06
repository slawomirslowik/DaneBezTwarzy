# Podsumowanie: Dodanie detektora LLM (PLLUM)

## 🎉 Zrealizowane zmiany

### 1. Nowy detektor LLM
**Plik:** `src/dane_bez_twarzy/detectors/llm_detector.py`

Utworzono kompletny detektor wykorzystujący model językowy PLLUM do wykrywania danych wrażliwych:
- Integracja z LangChain i OpenAI API
- Kontekstowe wykrywanie encji
- Automatyczne parsowanie odpowiedzi JSON z modelu
- Mapowanie typów encji
- Obsługa błędów i fallbacków

### 2. Aktualizacje kluczowych modułów

**`core/detector.py`:**
- Dodano property `llm_detector` z lazy loading
- Rozszerzono metodę `detect()` o wykrywanie przez LLM
- Dodano parametry inicjalizacji: `use_llm`, `llm_api_key`, `llm_base_url`, `llm_model_name`

**`core/anonymizer.py`:**
- Rozszerzono konstruktor o parametry LLM
- Przekazywanie parametrów LLM do detektora

**`detectors/__init__.py`:**
- Export LLMDetector

### 3. Zależności i konfiguracja

**`pyproject.toml`:**
- Dodano sekcję `[project.optional-dependencies.llm]`
- Zależności: `langchain-openai`, `langchain`

### 4. Dokumentacja

**Nowe pliki:**
- `LLM_USAGE.md` - Kompleksowa instrukcja użycia detektora LLM
- `examples/llm_usage.py` - Przykład praktycznego użycia
- `examples/README.md` - Przegląd wszystkich przykładów

**Zaktualizowane pliki:**
- `README.md` - Dodano sekcję o detektorze LLM
- `INSTALL.md` - Instrukcje instalacji zależności LLM

### 5. Testy

**`tests/test_llm_detector.py`:**
- Testy jednostkowe dla detektora LLM
- Mockowanie odpowiedzi API
- Testowanie edge cases

## 📦 Instalacja

```bash
# Zainstaluj z obsługą LLM
pip install -e ".[llm]"
```

## 🚀 Użycie

### Podstawowy przykład:

```python
from dane_bez_twarzy.core.anonymizer import Anonymizer
from dane_bez_twarzy.core.config import AnonymizationConfig, EntityType

config = AnonymizationConfig(
    entities=[EntityType.PERSON, EntityType.EMAIL, EntityType.ADDRESS],
    method="mask"
)

anonymizer = Anonymizer(
    config,
    use_llm=True,
    llm_api_key="c670f40b37e0495c845c63b1e548d95a",
    llm_base_url="https://apim-pllum-tst-pcn.azure-api.net/vllm/v1",
    llm_model_name="CYFRAGOVPL/pllum-12b-nc-chat-250715"
)

text = "Jan Kowalski mieszka przy ul. Kwiatowej 15 w Warszawie"
result = anonymizer.anonymize_text(text)
print(result.anonymized_text)
```

### Uruchomienie przykładu:

```bash
python examples/llm_usage.py
```

## ✨ Funkcjonalności

### Wykrywane typy danych:
- ✅ Imiona i nazwiska (PERSON)
- ✅ Adresy email (EMAIL)
- ✅ Numery telefonów (PHONE)
- ✅ PESEL
- ✅ NIP, REGON
- ✅ Adresy (ADDRESS)
- ✅ Karty kredytowe (CREDIT_CARD)
- ✅ IBAN
- ✅ Dowody osobiste, paszporty
- ✅ Nazwy organizacji (ORGANIZATION)
- ✅ Daty

### Zalety detektora LLM:
- 🧠 **Kontekstowe rozumienie** - analizuje znaczenie, nie tylko wzorce
- 🎯 **Wysoka dokładność** - model trenowany na dużych korpusach
- 🇵🇱 **Wsparcie polskiego** - PLLUM optymalny dla języka polskiego
- 🔄 **Elastyczność** - wykrywa nietypowe formaty

### Ograniczenia:
- ⏱️ Wolniejszy niż regex
- 💰 Wymaga dostępu do API (potencjalny koszt)
- 🌐 Wymaga połączenia internetowego

## 🔧 Architektura

```
Tekst
  ↓
EntityDetector
  ↓
┌─────────────────┬──────────────────┬─────────────────┐
│  RegexDetector  │  NLPDetector     │  LLMDetector    │
│  (PESEL, NIP)   │  (spaCy: names)  │  (PLLUM: all)   │
└─────────────────┴──────────────────┴─────────────────┘
  ↓
Deduplikacja i filtrowanie
  ↓
AnonymizationStrategy
  ↓
Zanonimizowany tekst
```

## 📊 Porównanie detektorów

| Detektor     | Szybkość | Dokładność | Offline | Instalacja |
|--------------|----------|------------|---------|------------|
| Regex        | ⚡⚡⚡    | ⭐⭐       | ✅      | Prosta     |
| spaCy NLP    | ⚡⚡      | ⭐⭐⭐     | ✅      | Średnia    |
| LLM (PLLUM)  | ⚡        | ⭐⭐⭐⭐   | ❌      | Prosta+API |

## 🧪 Testowanie

```bash
# Uruchom testy
pytest tests/test_llm_detector.py -v

# Uruchom wszystkie testy
pytest

# Z pokryciem kodu
pytest --cov=dane_bez_twarzy --cov-report=html
```

## 📚 Dokumentacja

- **LLM_USAGE.md** - Szczegółowa instrukcja użycia detektora LLM
- **README.md** - Główna dokumentacja projektu
- **INSTALL.md** - Instrukcje instalacji
- **examples/llm_usage.py** - Przykład praktyczny

## 🎯 Następne kroki (opcjonalne)

1. ✅ Cache'owanie odpowiedzi LLM dla optymalizacji kosztów
2. ✅ Batch processing dla wielu tekstów naraz
3. ✅ Konfiguracja timeout'ów i retry logic
4. ✅ Metryki i monitoring wywołań API
5. ✅ Fallback na inne detektory w razie błędu

## ⚠️ Ważne uwagi

1. **Klucz API:** Zabezpiecz klucz API (zmienne środowiskowe, secrets)
2. **Koszty:** Monitoruj użycie API i koszty
3. **Privacy:** Model wysyła dane do zewnętrznego API
4. **Rate limiting:** Uwzględnij limity API

## 💡 Przykładowe scenariusze użycia

### 1. Hybrydowe podejście (zalecane)
```python
# Regex dla prostych wzorców (PESEL, email)
# LLM dla złożonych (adresy, kontekst)
anonymizer = Anonymizer(config, use_llm=True)
```

### 2. Tylko LLM (maksymalna dokładność)
```python
config = AnonymizationConfig(use_nlp=False)  # Wyłącz spaCy
anonymizer = Anonymizer(config, use_llm=True)
```

### 3. Bez LLM (szybkie, offline)
```python
anonymizer = Anonymizer(config)  # Tylko regex i spaCy
```

## 📞 Kontakt

W razie pytań lub problemów, zobacz dokumentację lub utwórz issue na GitHub.

---

**Status:** ✅ Gotowe do użycia
**Wersja:** 0.1.0
**Data:** 2025-12-06
