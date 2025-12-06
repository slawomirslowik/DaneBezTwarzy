"""
Moduł konfiguracji dla biblioteki anonimizacji danych.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional, Dict


class EntityType(str, Enum):
    """Typy encji do wykrywania i anonimizacji."""
    
    PERSON = "PERSON"  # Imię i nazwisko
    EMAIL = "EMAIL"
    PHONE = "PHONE"
    PESEL = "PESEL"
    NIP = "NIP"
    REGON = "REGON"
    BANK_ACCOUNT = "BANK_ACCOUNT"
    CREDIT_CARD = "CREDIT_CARD"
    ADDRESS = "ADDRESS"
    DATE_OF_BIRTH = "DATE_OF_BIRTH"
    ID_CARD = "ID_CARD"  # Dowód osobisty
    PASSPORT = "PASSPORT"
    DRIVER_LICENSE = "DRIVER_LICENSE"
    LICENSE_PLATE = "LICENSE_PLATE"  # Numer rejestracyjny
    IP_ADDRESS = "IP_ADDRESS"
    URL = "URL"
    ORGANIZATION = "ORGANIZATION"
    LOCATION = "LOCATION"  # Lokalizacje geograficzne
    

class AnonymizationMethod(str, Enum):
    """Metody anonimizacji."""
    
    MASK = "mask"  # Maskowanie: Jan Kowalski -> *** ********
    PSEUDONYMIZE = "pseudonymize"  # Pseudonimizacja: Jan Kowalski -> Osoba_A
    HASH = "hash"  # Haszowanie: Jan Kowalski -> a3f5b8c9...
    GENERALIZE = "generalize"  # Generalizacja: 01/15/1990 -> 1990
    REDACT = "redact"  # Usuwanie: Jan Kowalski -> [USUNIĘTO]
    ENCRYPT = "encrypt"  # Szyfrowanie (odwracalne)
    

@dataclass
class AnonymizationConfig:
    """Konfiguracja procesu anonimizacji."""
    
    # Język dokumentu
    language: str = "pl"
    
    # Metoda anonimizacji
    method: AnonymizationMethod = AnonymizationMethod.MASK
    
    # Typy encji do anonimizacji (None = wszystkie)
    entities: Optional[List[EntityType]] = None
    
    # Parametry maskowania
    mask_char: str = "*"
    preserve_length: bool = True
    preserve_structure: bool = True  # Zachowaj strukturę (np. format telefonu)
    
    # Parametry pseudonimizacji
    seed: Optional[int] = None  # Seed dla powtarzalnych pseudonimów
    pseudonym_prefix: str = "Osoba"
    
    # Parametry haszowania
    hash_algorithm: str = "sha256"
    hash_salt: Optional[str] = None
    
    # Parametry szyfrowania
    encryption_key: Optional[str] = None
    
    # Własne wzorce regex
    custom_patterns: Dict[str, str] = field(default_factory=dict)
    
    # Wykluczenia (słowa/wzorce do pominięcia)
    exclusions: List[str] = field(default_factory=list)
    
    # Opcje przetwarzania
    case_sensitive: bool = False
    detect_context: bool = True  # Użyj kontekstu do lepszego wykrywania
    min_confidence: float = 0.7  # Minimalna pewność wykrycia (0-1)
    
    # Opcje dla NLP
    use_nlp: bool = False  # Domyślnie wyłączone (szybsze, bez limitu rozmiaru)
    nlp_model: str = "pl_core_news_lg"
    
    # Raportowanie
    generate_report: bool = True
    report_format: str = "json"  # json, html, txt
    
    # Logowanie
    verbose: bool = False
    log_level: str = "INFO"
    
    def __post_init__(self) -> None:
        """Walidacja i normalizacja konfiguracji."""
        if self.entities is None:
            self.entities = list(EntityType)
        
        if isinstance(self.method, str):
            self.method = AnonymizationMethod(self.method)
        
        # Konwersja stringów na EntityType
        self.entities = [
            EntityType(e) if isinstance(e, str) else e 
            for e in self.entities
        ]
        
        if not 0 <= self.min_confidence <= 1:
            raise ValueError("min_confidence musi być w zakresie 0-1")
        
        if self.method == AnonymizationMethod.ENCRYPT and not self.encryption_key:
            raise ValueError("encryption_key jest wymagany dla metody ENCRYPT")
