"""
Detektor placeholderów w formacie [name], [email], [phone] itp.
Używany do wykrywania i anonimizacji szablonów dokumentów.
"""

from typing import List
import re
import logging

from dane_bez_twarzy.core.config import AnonymizationConfig, EntityType
from dane_bez_twarzy.core.detector import Entity


class PlaceholderDetector:
    """
    Wykrywa placeholdery w formacie [typ_danych].
    Przydatne do anonimizacji szablonów i dokumentów testowych.
    """
    
    def __init__(self, config: AnonymizationConfig):
        """
        Inicjalizacja detektora placeholderów.
        
        Args:
            config: Konfiguracja anonimizacji.
        """
        self.config = config
        self.logger = logging.getLogger(__name__)
        
        # Mapowanie placeholderów na typy encji
        self.placeholder_mapping = {
            # Dane osobowe
            r'\[name\]': EntityType.PERSON,
            r'\[surname\]': EntityType.PERSON,
            r'\[first[\s_-]?name\]': EntityType.PERSON,
            r'\[last[\s_-]?name\]': EntityType.PERSON,
            r'\[full[\s_-]?name\]': EntityType.PERSON,
            
            # Kontakt
            r'\[email\]': EntityType.EMAIL,
            r'\[e[\s_-]?mail\]': EntityType.EMAIL,
            r'\[phone\]': EntityType.PHONE,
            r'\[telephone\]': EntityType.PHONE,
            r'\[tel\]': EntityType.PHONE,
            r'\[mobile\]': EntityType.PHONE,
            r'\[address\]': EntityType.ADDRESS,
            r'\[city\]': EntityType.LOCATION,
            r'\[street\]': EntityType.ADDRESS,
            
            # Identyfikatory
            r'\[pesel\]': EntityType.PESEL,
            r'\[nip\]': EntityType.NIP,
            r'\[regon\]': EntityType.REGON,
            r'\[document[\s_-]?number\]': EntityType.ID_CARD,
            r'\[passport\]': EntityType.PASSPORT,
            r'\[id[\s_-]?card\]': EntityType.ID_CARD,
            
            # Finansowe
            r'\[bank[\s_-]?account\]': EntityType.BANK_ACCOUNT,
            r'\[credit[\s_-]?card\]': EntityType.CREDIT_CARD,
            r'\[credit[\s_-]?card[\s_-]?number\]': EntityType.CREDIT_CARD,
            r'\[iban\]': EntityType.BANK_ACCOUNT,
            
            # Daty
            r'\[date\]': EntityType.DATE,
            r'\[birth[\s_-]?date\]': EntityType.DATE_OF_BIRTH,
            r'\[date[\s_-]?of[\s_-]?birth\]': EntityType.DATE_OF_BIRTH,
            r'\[dob\]': EntityType.DATE_OF_BIRTH,
            
            # Inne
            r'\[age\]': EntityType.AGE,
            r'\[sex\]': EntityType.SEX,
            r'\[gender\]': EntityType.SEX,
            r'\[username\]': EntityType.USERNAME,
            r'\[login\]': EntityType.USERNAME,
            r'\[password\]': EntityType.SECRET,
            r'\[secret\]': EntityType.SECRET,
            r'\[company\]': EntityType.ORGANIZATION,
            r'\[organization\]': EntityType.ORGANIZATION,
            r'\[job[\s_-]?title\]': EntityType.JOB_TITLE,
            r'\[license[\s_-]?plate\]': EntityType.LICENSE_PLATE,
            r'\[vehicle[\s_-]?registration\]': EntityType.LICENSE_PLATE,
        }
    
    def detect(self, text: str) -> List[Entity]:
        """
        Wykrywa placeholdery w tekście.
        
        Args:
            text: Tekst do analizy.
            
        Returns:
            Lista wykrytych placeholderów jako encji.
        """
        entities = []
        
        for pattern, entity_type in self.placeholder_mapping.items():
            # Sprawdź czy ten typ encji jest w konfiguracji
            if entity_type not in self.config.entities:
                continue
            
            # Kompiluj pattern z flagą case-insensitive
            regex = re.compile(pattern, re.IGNORECASE)
            
            # Szukaj wszystkich wystąpień
            for match in regex.finditer(text):
                entity = Entity(
                    text=match.group(),
                    type=entity_type,
                    start=match.start(),
                    end=match.end(),
                    confidence=1.0,  # Placeholdery są zawsze pewne
                    metadata={
                        "detector": "placeholder",
                        "pattern": pattern,
                        "placeholder_name": match.group()  # Zachowaj oryginalną nazwę
                    }
                )
                entities.append(entity)
                
                self.logger.debug(
                    f"Znaleziono placeholder: '{match.group()}' "
                    f"jako {entity_type.value}"
                )
        
        return entities
