"""
Detektor dla polskich wzorców (kontekstowy).
"""

from typing import List
import logging

from dane_bez_twarzy.core.config import AnonymizationConfig, EntityType
from dane_bez_twarzy.core.detector import Entity


class PolishDetector:
    """
    Detektor specjalizowany dla polskich danych.
    Używa kontekstu i heurystyk specyficznych dla języka polskiego.
    """
    
    def __init__(self, config: AnonymizationConfig):
        """
        Inicjalizacja detektora polskiego.
        
        Args:
            config: Konfiguracja anonimizacji.
        """
        self.config = config
        self.logger = logging.getLogger(__name__)
        
        # Słowa kluczowe sugerujące dane osobowe
        self.context_keywords = {
            EntityType.PERSON: ["pan", "pani", "dr", "prof", "mgr", "inż"],
            EntityType.PESEL: ["pesel", "nr pesel", "numer pesel"],
            EntityType.NIP: ["nip", "nr nip", "numer nip"],
            EntityType.PHONE: ["tel", "telefon", "tel.", "kom", "komórka"],
            EntityType.EMAIL: ["email", "e-mail", "mail", "adres email"],
            EntityType.ADDRESS: ["ul.", "ulica", "os.", "osiedle", "al.", "aleja"],
        }
    
    def detect(self, text: str) -> List[Entity]:
        """
        Wykrywa encje używając kontekstu polskiego języka.
        
        Args:
            text: Tekst do analizy.
            
        Returns:
            Lista wykrytych encji.
        """
        entities = []
        
        # Tutaj można dodać bardziej zaawansowane wykrywanie
        # na podstawie kontekstu polskiego języka
        
        # Przykład: wykrywanie adresów po słowach kluczowych
        if EntityType.ADDRESS in self.config.entities:
            entities.extend(self._detect_addresses(text))
        
        return entities
    
    def _detect_addresses(self, text: str) -> List[Entity]:
        """
        Wykrywa polskie adresy.
        
        Args:
            text: Tekst do analizy.
            
        Returns:
            Lista wykrytych adresów.
        """
        # Uproszczona implementacja
        # W pełnej wersji można użyć bardziej zaawansowanych metod
        import re
        
        entities = []
        
        # Wzorzec dla polskiego adresu
        address_pattern = re.compile(
            r'(?:ul\.|ulica|os\.|osiedle|al\.|aleja)\s+[A-ZĄĆĘŁŃÓŚŹŻ][a-ząćęłńóśźż]+(?:\s+\d+(?:/\d+)?)?',
            re.IGNORECASE
        )
        
        for match in address_pattern.finditer(text):
            entity = Entity(
                text=match.group(0),
                type=EntityType.ADDRESS,
                start=match.start(),
                end=match.end(),
                confidence=0.8,
                metadata={"detector": "polish"}
            )
            entities.append(entity)
        
        return entities
