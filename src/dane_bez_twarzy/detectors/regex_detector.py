"""
Detektor używający wyrażeń regularnych.
"""

import re
from typing import List
import logging

from dane_bez_twarzy.core.config import AnonymizationConfig, EntityType
from dane_bez_twarzy.core.detector import Entity
from dane_bez_twarzy.utils.patterns import (
    get_patterns_for_entity_type,
    ValidationPatterns
)


class RegexDetector:
    """Wykrywa encje używając wyrażeń regularnych."""
    
    def __init__(self, config: AnonymizationConfig):
        """
        Inicjalizacja detektora regex.
        
        Args:
            config: Konfiguracja anonimizacji.
        """
        self.config = config
        self.logger = logging.getLogger(__name__)
        self.validators = ValidationPatterns()
    
    def detect(self, text: str) -> List[Entity]:
        """
        Wykrywa encje w tekście używając regex.
        
        Args:
            text: Tekst do analizy.
            
        Returns:
            Lista wykrytych encji.
        """
        entities = []
        
        for entity_type in self.config.entities:
            # Pobierz wzorce dla typu encji
            patterns = get_patterns_for_entity_type(entity_type.value)
            
            # Dodaj własne wzorce użytkownika
            if entity_type.value in self.config.custom_patterns:
                patterns[f"custom_{entity_type.value}"] = re.compile(
                    self.config.custom_patterns[entity_type.value]
                )
            
            # Szukaj dopasowań
            for pattern_name, pattern in patterns.items():
                for match in pattern.finditer(text):
                    matched_text = match.group(0)
                    
                    # Walidacja (jeśli dostępna)
                    if not self._validate(entity_type, matched_text):
                        continue
                    
                    entity = Entity(
                        text=matched_text,
                        type=entity_type,
                        start=match.start(),
                        end=match.end(),
                        confidence=1.0,
                        metadata={"detector": "regex", "pattern": pattern_name}
                    )
                    entities.append(entity)
        
        return entities
    
    def _validate(self, entity_type: EntityType, text: str) -> bool:
        """
        Waliduje wykryty tekst (np. sprawdza checksumę).
        
        Args:
            entity_type: Typ encji.
            text: Tekst do walidacji.
            
        Returns:
            True jeśli tekst jest poprawny.
        """
        validators = {
            EntityType.PESEL: self.validators.validate_pesel,
            EntityType.NIP: self.validators.validate_nip,
            EntityType.REGON: self.validators.validate_regon,
            EntityType.CREDIT_CARD: self.validators.validate_credit_card,
        }
        
        validator = validators.get(entity_type)
        if validator:
            try:
                return validator(text)
            except Exception as e:
                self.logger.debug(f"Błąd walidacji {entity_type}: {e}")
                return False
        
        return True  # Brak walidatora = akceptuj
