# Detektory - Podsumowanie

## Przegląd

Projekt **Dane Bez Twarzy** wykorzystuje **5 detektorów** działających równolegle do wykrywania danych osobowych. Każdy detektor ma różne podejście, zależności i charakterystykę wydajnościową.

---

## 1. **PlaceholderDetector** ✅

### Opis
Wykrywa placeholdery w notacji kwadratowych nawiasów używane w templatech i plikach treningowych (np. format NASK).

### Wykrywane wzorce
- `[name]`, `[surname]`, `[email]`, `[phone]`
- `[pesel]`, `[nip]`, `[regon]`, `[address]`, `[city]`
- `[birth-date]`, `[age]`, `[sex]`, `[job-title]`
- 30+ typów placeholderów

### Biblioteki
- `re` (regex - standardowa Python)
- `logging` (standardowa Python)
- **Brak zewnętrznych zależności**

### Charakterystyka
- **Pewność**: 1.0 (100% - najwyższa)
- **Szybkość**: ⚡⚡⚡⚡⚡ (błyskawiczny)
- **Rozmiar**: ~5 KB
- **Status**: Zawsze aktywny

### Zastosowanie
Idealny dla dokumentów treningowych AI/ML, templatech emaili, plików testowych.

---

## 2. **RegexDetector** ✅

### Opis
Wykrywa dane osobowe przez deterministyczne wyrażenia regularne (regex).

### Wykrywane wzorce
- **PESEL**: `90010112345`
- **NIP**: `123-456-78-90`, `1234567890`
- **REGON**: `123456789`, `12345678901234`
- **Email**: `jan.kowalski@example.com`
- **Telefon**: `+48 123 456 789`, `123-456-789`
- **Konto bankowe**: `12 3456 7890 1234 5678 9012 3456`
- **Karty płatnicze**: Visa, Mastercard, Amex
- **URL**, **IP Address**

### Biblioteki
- `re` (regex - standardowa Python)
- `logging` (standardowa Python)
- **Brak zewnętrznych zależności**

### Charakterystyka
- **Pewność**: 0.8-0.95 (wysoka)
- **Szybkość**: ⚡⚡⚡⚡⚡ (błyskawiczny)
- **Rozmiar**: ~10 KB
- **Status**: Zawsze aktywny

### Zastosowanie
Uniwersalny detektor dla strukturalnych danych (numery, formaty).

---

## 3. **PolishDetector** ✅

### Opis
Specjalizowany detektor dla polskich wzorców z użyciem heurystyk i kontekstu.

### Wykrywane wzorce
- **Adresy**: `ul. Kwiatowa 15`, `al. Jerozolimskie 123/45`
- **Kody pocztowe**: `00-001`, `12-345`
- **Numery dokumentów**: dowód osobisty, prawo jazdy
- **Polskie imiona/nazwiska** (słownik + kontekst)
- **Tytuły**: Pan, Pani, Dr, Prof, Mgr, Inż

### Biblioteki
- `logging` (standardowa Python)
- `typing` (standardowa Python)
- **Brak zewnętrznych zależności**

### Charakterystyka
- **Pewność**: 0.7-0.9 (dobra)
- **Szybkość**: ⚡⚡⚡⚡ (bardzo szybki)
- **Rozmiar**: ~15 KB
- **Status**: Aktywny automatycznie gdy `language="pl"`

### Zastosowanie
Dokumenty w języku polskim (urzędowe, CV, korespondencja).

---

## 4. **NLPDetector** ⚠️

### Opis
Zaawansowany detektor używający Named Entity Recognition (NER) przez spaCy do analizy kontekstowej.

### Wykrywane wzorce
- **Imiona i nazwiska**: Jan Kowalski, Anna Nowak
- **Organizacje**: Microsoft, Google Poland
- **Lokalizacje**: Warszawa, Kraków, ul. Marszałkowska
- Rozpoznaje kontekst (nie tylko wzorce)

### Biblioteki
- **`spacy`** (główna biblioteka NLP) - ~10 MB
- **`pl_core_news_lg`** (model polski) - ~500 MB
- `logging` (standardowa Python)

### Charakterystyka
- **Pewność**: 0.6-0.95 (bardzo dobra, zależy od kontekstu)
- **Szybkość**: ⚡⚡ (wolniejszy, ~100-500 ms/dokument)
- **Rozmiar**: ~500 MB (model)
- **Status**: Wymaga flagi `--use-nlp` lub `use_nlp=True`

### Zastosowanie
Dokumenty z tekstem naturalnym gdzie imiona/nazwiska nie mają określonego formatu.

### Instalacja
```bash
pip install spacy
python -m spacy download pl_core_news_lg
```

---

## 5. **LLMDetector** 🔥

### Opis
Najbardziej zaawansowany detektor używający modelu językowego PLLUM (12B parametrów) przez API.

### Wykrywane wzorce
- **Wszystko co wykrywają pozostałe detektory**
- **Dane wrażliwe w kontekście**: pseudonimy, przezwiska
- **Informacje ukryte**: „Jej brat to..." (inferencja)
- **Niestandarowe formaty**: kreatywne zapisy danych
- Najlepsza precyzja dzięki rozumieniu języka naturalnego

### Biblioteki
- **`langchain-openai`** (integracja z LLM) - ~20 MB
- **ChatOpenAI** (klient API)
- `json`, `re`, `logging` (standardowe Python)

### Charakterystyka
- **Pewność**: 0.85-0.98 (najwyższa)
- **Szybkość**: ⚡ (wolny, ~1-5s/dokument, zależy od API)
- **Rozmiar**: ~20 MB (biblioteka) + API zdalnie
- **Status**: Wymaga flagi `--use-llm` i klucza API
- **Chunking**: Automatyczny podział dużych plików (3000 znaków/fragment)

### Zastosowanie
Krytyczne dokumenty wymagające maksymalnej precyzji (medyczne, prawne, HR).

### Instalacja
```bash
pip install langchain-openai
```

### Użycie
```bash
dane-bez-twarzy anonymize input.txt -o output.txt \
  --use-llm \
  --llm-api-key "c670f40b37e0495c845c63b1e548d95a"
```

---

## Porównanie

| Detektor | Biblioteki | Rozmiar | Szybkość | Pewność | Status |
|----------|-----------|---------|----------|---------|--------|
| **Placeholder** | Brak (tylko stdlib) | ~5 KB | ⚡⚡⚡⚡⚡ | 1.0 | Zawsze aktywny |
| **Regex** | Brak (tylko stdlib) | ~10 KB | ⚡⚡⚡⚡⚡ | 0.8-0.95 | Zawsze aktywny |
| **Polish** | Brak (tylko stdlib) | ~15 KB | ⚡⚡⚡⚡ | 0.7-0.9 | Auto (gdy `lang=pl`) |
| **NLP** | **spaCy + model** | ~500 MB | ⚡⚡ | 0.6-0.95 | `--use-nlp` |
| **LLM** | **langchain-openai** | ~20 MB | ⚡ (API) | 0.85-0.98 | `--use-llm` + API key |

---

## Różnice kluczowe

### Podejście do detekcji

1. **Placeholder, Regex, Polish**: Wzorce deterministyczne
   - Szybkie, przewidywalne
   - Nie wymagają ML/AI
   - Działają offline

2. **NLP**: Machine Learning (spaCy)
   - Rozumie kontekst
   - Wymaga modelu (500 MB)
   - Działa offline po pobraniu modelu

3. **LLM**: Large Language Model (PLLUM)
   - Najinteligentniejszy (12B parametrów)
   - Rozumie język naturalny i inferencję
   - Wymaga API (działa online)

### Zależności

- **Bez zależności** (3 detektory): Placeholder, Regex, Polish
  - Idealne dla wersji LITE standalone EXE (~50 MB)
  
- **Z zależnościami** (2 detektory): NLP, LLM
  - Wersja FULL z NLP: ~600 MB (standalone EXE)
  - LLM zawsze wymaga API (nie można spakować modelu)

### Przypadki użycia

| Scenariusz | Rekomendowane detektory |
|-----------|------------------------|
| **Szybkie przetwarzanie** | Placeholder + Regex + Polish |
| **CV/dokumenty urzędowe** | + NLP |
| **Dokumenty medyczne/prawne** | + LLM |
| **Offline/standalone** | Placeholder + Regex + Polish (+ NLP jeśli FULL) |
| **Maksymalna precyzja** | Wszystkie 5 detektorów |

---

## Strategia wyboru

```bash
# Domyślnie (szybkie, offline)
dane-bez-twarzy anonymize input.txt -o output.txt

# Z NLP (dokładniejsze imiona/nazwiska)
dane-bez-twarzy anonymize input.txt -o output.txt --use-nlp

# Z LLM (maksymalna precyzja)
dane-bez-twarzy anonymize input.txt -o output.txt --use-llm --llm-api-key "klucz"

# ALL-IN (wszystkie detektory)
dane-bez-twarzy anonymize input.txt -o output.txt \
  --use-nlp --use-llm --llm-api-key "klucz"
```

---

## Architektura

Wszystkie detektory implementują interfejs:
```python
class Detector:
    def detect(self, text: str) -> List[Entity]:
        """Wykrywa encje w tekście."""
        pass
```

Wyniki są łączone i deduplikowane w `Anonymizer.detect()` z priorytetyzacją:
1. Wyższa pewność (confidence)
2. Dłuższy tekst (gdy nakładanie)
3. Późniejszy detektor (przy równości)

---

**Podsumowanie**: Projekt oferuje elastyczny system detektorów - od szybkich regex (bez zależności) po zaawansowany LLM (API), pozwalając dostosować trade-off między szybkością, rozmiarem, kosztem a precyzją.
