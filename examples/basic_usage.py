"""
Przykład użycia biblioteki Dane Bez Twarzy.
"""

from dane_bez_twarzy import Anonymizer, AnonymizationConfig, EntityType


def example_basic():
    """Podstawowy przykład użycia."""
    print("=" * 60)
    print("PRZYKŁAD 1: Podstawowa anonimizacja")
    print("=" * 60)
    
    # Tekst z danymi osobowymi
    text = """
    Dane kontaktowe:
    Jan Kowalski
    PESEL: 90010112345
    Email: jan.kowalski@example.com
    Tel: +48 123 456 789
    """
    
    # Konfiguracja
    config = AnonymizationConfig(
        language="pl",
        method="mask",
        preserve_length=True
    )
    
    # Anonimizacja
    anonymizer = Anonymizer(config)
    result = anonymizer.anonymize_text(text)
    
    print("Oryginalny tekst:")
    print(text)
    print("\nZanonimizowany tekst:")
    print(result)


def example_pseudonymize():
    """Przykład pseudonimizacji."""
    print("\n" + "=" * 60)
    print("PRZYKŁAD 2: Pseudonimizacja")
    print("=" * 60)
    
    text = """
    Spotkanie z Janem Kowalskim (jan.kowalski@firma.pl) i 
    Anną Nowak (anna.nowak@firma.pl) zaplanowane na 15.01.2024.
    Jan Kowalski przekaże dokumenty.
    """
    
    config = AnonymizationConfig(
        language="pl",
        method="pseudonymize",
        seed=12345  # Dla powtarzalności
    )
    
    anonymizer = Anonymizer(config)
    result = anonymizer.anonymize_text(text)
    
    print("Oryginalny tekst:")
    print(text)
    print("\nZanonimizowany tekst (pseudonimy):")
    print(result)


def example_selective():
    """Przykład selektywnej anonimizacji."""
    print("\n" + "=" * 60)
    print("PRZYKŁAD 3: Selektywna anonimizacja")
    print("=" * 60)
    
    text = """
    Firma XYZ Sp. z o.o.
    ul. Kwiatowa 15, 00-001 Warszawa
    NIP: 123-456-78-90
    REGON: 123456789
    
    Kontakt: biuro@xyz.pl, tel. 22 123 45 67
    """
    
    # Anonimizuj tylko numery identyfikacyjne
    config = AnonymizationConfig(
        language="pl",
        method="generalize",
        entities=[EntityType.NIP, EntityType.REGON]
    )
    
    anonymizer = Anonymizer(config)
    result = anonymizer.anonymize_text(text)
    
    print("Oryginalny tekst:")
    print(text)
    print("\nZanonimizowany tekst (tylko NIP i REGON):")
    print(result)


def example_detect():
    """Przykład wykrywania encji."""
    print("\n" + "=" * 60)
    print("PRZYKŁAD 4: Wykrywanie encji")
    print("=" * 60)
    
    text = """
    Jan Kowalski, PESEL: 90010112345
    Email: jan.kowalski@example.com
    Telefon: +48 123-456-789
    Adres: ul. Kwiatowa 15, Warszawa
    """
    
    config = AnonymizationConfig(language="pl")
    anonymizer = Anonymizer(config)
    
    entities = anonymizer.detect_entities(text)
    
    print("Wykryte encje:")
    for entity in entities:
        print(f"  - {entity['type']}: '{entity['text']}' "
              f"(pozycja: {entity['start']}-{entity['end']}, "
              f"pewność: {entity['confidence']:.2f})")


def example_file():
    """Przykład anonimizacji pliku."""
    print("\n" + "=" * 60)
    print("PRZYKŁAD 5: Anonimizacja pliku")
    print("=" * 60)
    
    # Utwórz przykładowy plik
    test_file = "test_data.txt"
    with open(test_file, 'w', encoding='utf-8') as f:
        f.write("""
        POUFNE DANE
        
        Pracownik: Jan Kowalski
        PESEL: 90010112345
        Email: jan.kowalski@firma.pl
        Telefon: 123-456-789
        
        Adres: ul. Testowa 1, 00-001 Warszawa
        """)
    
    # Anonimizuj
    config = AnonymizationConfig(language="pl", method="mask")
    anonymizer = Anonymizer(config)
    
    output_file = anonymizer.anonymize_file(test_file)
    
    print(f"Plik '{test_file}' został zanonimizowany.")
    print(f"Wynik zapisany w: {output_file}")
    
    # Wyświetl wynik
    with open(output_file, 'r', encoding='utf-8') as f:
        print("\nZanonimizowana zawartość:")
        print(f.read())


def example_custom_patterns():
    """Przykład z własnymi wzorcami."""
    print("\n" + "=" * 60)
    print("PRZYKŁAD 6: Własne wzorce")
    print("=" * 60)
    
    text = """
    Numer zamówienia: ZAM-2024-001234
    Kod produktu: PROD-XYZ-789
    """
    
    config = AnonymizationConfig(
        language="pl",
        method="mask",
        custom_patterns={
            "ORDER_NUMBER": r"ZAM-\d{4}-\d{6}",
            "PRODUCT_CODE": r"PROD-[A-Z]{3}-\d{3}"
        }
    )
    
    anonymizer = Anonymizer(config)
    result = anonymizer.anonymize_text(text)
    
    print("Oryginalny tekst:")
    print(text)
    print("\nZanonimizowany tekst (własne wzorce):")
    print(result)


if __name__ == "__main__":
    # Uruchom wszystkie przykłady
    example_basic()
    example_pseudonymize()
    example_selective()
    example_detect()
    example_file()
    example_custom_patterns()
    
    print("\n" + "=" * 60)
    print("Wszystkie przykłady zakończone!")
    print("=" * 60)
