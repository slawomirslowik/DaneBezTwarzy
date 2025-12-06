"""
Szybki test biblioteki Dane Bez Twarzy.
"""

from dane_bez_twarzy import Anonymizer, AnonymizationConfig, EntityType

def test_basic():
    """Test podstawowej funkcjonalności."""
    print("=" * 60)
    print("TEST 1: Maskowanie danych")
    print("=" * 60)
    
    config = AnonymizationConfig(
        language="pl",
        method="mask",
        use_nlp=False,  # Bez spaCy - używamy tylko regex (szybsze, bez limitu)
        verbose=True    # Więcej informacji o przetwarzaniu
    )
    
    anonymizer = Anonymizer(config)
    
    test_cases = [
        "PESEL: 90010112345",
        "NIP: 123-456-78-90",
        "Email: jan.kowalski@firma.pl",
        "Telefon: +48 123 456 789",
        "Konto: 12 3456 7890 1234 5678 9012 3456",
    ]
    
    for test in test_cases:
        result = anonymizer.anonymize_text(test)
        print(f"Oryginalny: {test}")
        print(f"Anonimizowany: {result}")
        print()


def test_detection():
    """Test wykrywania encji."""
    print("=" * 60)
    print("TEST 2: Wykrywanie encji")
    print("=" * 60)
    
    config = AnonymizationConfig(language="pl", use_nlp=False)
    anonymizer = Anonymizer(config)
    
    text = """
    Dane osobowe:
    PESEL: 90010112345
    NIP: 1234567890
    Email: test@example.com
    Telefon: 123-456-789
    """
    
    entities = anonymizer.detect_entities(text)
    
    print(f"Znaleziono {len(entities)} encji:")
    for entity in entities:
        print(f"  - {entity['type']}: '{entity['text']}' (pewność: {entity['confidence']:.2f})")


def test_methods():
    """Test różnych metod anonimizacji."""
    print("\n" + "=" * 60)
    print("TEST 3: Różne metody anonimizacji")
    print("=" * 60)
    
    text = "Jan Kowalski, PESEL: 90010112345, jan@example.com"
    
    methods = ["mask", "pseudonymize", "generalize", "redact"]
    
    for method in methods:
        config = AnonymizationConfig(
            language="pl",
            method=method,
            use_nlp=False
        )
        anonymizer = Anonymizer(config)
        result = anonymizer.anonymize_text(text)
        
        print(f"\n{method.upper()}:")
        print(f"  Wynik: {result}")


def test_selective():
    """Test selektywnej anonimizacji."""
    print("\n" + "=" * 60)
    print("TEST 4: Selektywna anonimizacja (tylko PESEL)")
    print("=" * 60)
    
    text = "Pracownik: PESEL 90010112345, Email: jan@firma.pl, Tel: 123456789"
    
    config = AnonymizationConfig(
        language="pl",
        method="mask",
        entities=[EntityType.PESEL],  # Tylko PESEL
        use_nlp=False
    )
    
    anonymizer = Anonymizer(config)
    result = anonymizer.anonymize_text(text)
    
    print(f"Oryginalny: {text}")
    print(f"Zanonimizowany: {result}")
    print("(Tylko PESEL został zamaskowany)")


def test_file():
    """Test anonimizacji pliku."""
    print("\n" + "=" * 60)
    print("TEST 5: Anonimizacja pliku")
    print("=" * 60)
    
    # Utwórz testowy plik
    test_file = "test_input.txt"
    with open(test_file, 'w', encoding='utf-8') as f:
        f.write("""
DANE TESTOWE

Pracownik: Jan Kowalski
PESEL: 90010112345
Email: jan.kowalski@firma.pl
Telefon: +48 123 456 789
NIP firmy: 123-456-78-90

Adres: ul. Testowa 1, 00-001 Warszawa
        """)
    
    print(f"Utworzono plik: {test_file}")
    
    # Anonimizuj
    config = AnonymizationConfig(language="pl", method="mask", use_nlp=False)
    anonymizer = Anonymizer(config)
    
    output_file = anonymizer.anonymize_file(test_file)
    
    print(f"Plik zanonimizowany: {output_file}")
    
    # Wyświetl wynik
    with open(output_file, 'r', encoding='utf-8') as f:
        content = f.read()
        print("\nZanonimizowana zawartość:")
        print(content)


if __name__ == "__main__":
    try:
        test_basic()
        test_detection()
        test_methods()
        test_selective()
        test_file()
        
        print("\n" + "=" * 60)
        print("✓ WSZYSTKIE TESTY ZAKOŃCZONE POMYŚLNIE!")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n✗ BŁĄD: {e}")
        import traceback
        traceback.print_exc()
