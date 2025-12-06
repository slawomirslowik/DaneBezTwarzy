"""
Przykład użycia detektora LLM (PLLUM) do wykrywania danych wrażliwych.
"""

from dane_bez_twarzy.core.config import AnonymizationConfig, EntityType, AnonymizationMethod
from dane_bez_twarzy.core.detector import EntityDetector
from dane_bez_twarzy.core.anonymizer import Anonymizer


def main():
    # Tekst do anonimizacji z różnymi danymi wrażliwymi
    text = """
    Dane kontaktowe:
    Jan Kowalski, PESEL: 92101012345
    Email: jan.kowalski@example.com
    Telefon: +48 123 456 789
    Adres: ul. Kwiatowa 15, 00-001 Warszawa
    
    Informacje finansowe:
    Numer karty: 4532 1234 5678 9012
    IBAN: PL61 1090 1014 0000 0712 1981 2874
    NIP: 123-456-78-90
    
    Firma XYZ Sp. z o.o. zatrudnia 50 pracowników.
    Data urodzenia: 01.10.1992
    """
    
    print("=" * 80)
    print("Przykład użycia detektora LLM (PLLUM)")
    print("=" * 80)
    print("\nTekst oryginalny:")
    print(text)
    print("\n" + "=" * 80)
    
    # Konfiguracja - wykrywanie wszystkich typów encji
    config = AnonymizationConfig(
        entities=[
            EntityType.PERSON,
            EntityType.EMAIL,
            EntityType.PHONE,
            EntityType.PESEL,
            EntityType.NIP,
            EntityType.ADDRESS,
            EntityType.CREDIT_CARD,
            EntityType.IBAN,
            EntityType.ORGANIZATION,
            EntityType.DATE,
        ],
        method=AnonymizationMethod.MASK,
        use_nlp=False,  # Wyłączamy spaCy, używamy tylko LLM
        language="pl"
    )
    
    # OPCJA 1: Użycie tylko detektora LLM
    print("\n1. DETEKCJA UŻYWAJĄC LLM:")
    print("-" * 80)
    
    # Inicjalizacja detektora z LLM
    detector = EntityDetector(
        config,
        use_llm=True,
        llm_api_key="c670f40b37e0495c845c63b1e548d95a",  # Twój klucz API
        llm_base_url="https://apim-pllum-tst-pcn.azure-api.net/vllm/v1",
        llm_model_name="CYFRAGOVPL/pllum-12b-nc-chat-250715"
    )
    
    # Wykryj encje
    entities = detector.detect(text)
    
    print(f"\nWykryto {len(entities)} encji:")
    for i, entity in enumerate(entities, 1):
        print(f"\n{i}. {entity.type.value}:")
        print(f"   Tekst: '{entity.text}'")
        print(f"   Pozycja: {entity.start}-{entity.end}")
        print(f"   Pewność: {entity.confidence:.2f}")
        if entity.metadata:
            print(f"   Metadata: {entity.metadata}")
    
    # OPCJA 2: Pełna anonimizacja używając LLM
    print("\n\n2. ANONIMIZACJA UŻYWAJĄC LLM:")
    print("-" * 80)
    
    anonymizer = Anonymizer(
        config,
        use_llm=True,
        llm_api_key="c670f40b37e0495c845c63b1e548d95a",
        llm_base_url="https://apim-pllum-tst-pcn.azure-api.net/vllm/v1",
        llm_model_name="CYFRAGOVPL/pllum-12b-nc-chat-250715"
    )
    
    # Anonimizuj tekst
    result = anonymizer.anonymize_text(text)
    
    print("\nTekst zanonimizowany:")
    print(result.anonymized_text)
    
    print("\n\nStatystyki:")
    print(f"  - Wykryte encje: {len(result.entities)}")
    print(f"  - Zanonimizowane encje: {result.entities_count}")
    
    # Grupuj encje według typu
    entities_by_type = {}
    for entity in result.entities:
        entity_type = entity.type.value
        if entity_type not in entities_by_type:
            entities_by_type[entity_type] = []
        entities_by_type[entity_type].append(entity)
    
    print("\nWykryte encje według typu:")
    for entity_type, entity_list in sorted(entities_by_type.items()):
        print(f"  - {entity_type}: {len(entity_list)}")
    
    print("\n" + "=" * 80)
    print("Zakończono przykład użycia detektora LLM")
    print("=" * 80)


if __name__ == "__main__":
    main()
