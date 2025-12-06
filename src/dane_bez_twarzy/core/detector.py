"""
Moduł wykrywania encji (PII) w tekście.
"""

from dataclasses import dataclass
from typing import List, Optional
import logging

from dane_bez_twarzy.core.config import AnonymizationConfig, EntityType


@dataclass
class Entity:
    """Reprezentacja wykrytej encji."""
    
    text: str
    type: EntityType
    start: int
    end: int
    confidence: float = 1.0
    metadata: Optional[dict] = None


class EntityDetector:
    """
    Detektor encji w tekście używający wielu metod:
    - Wyrażenia regularne (szybkie, deterministyczne)
    - NLP/NER (kontekstowe, dla imion/nazwisk)
    - Własne wzorce użytkownika
    """
    
    def __init__(self, config: AnonymizationConfig, use_llm: bool = False,
                 llm_api_key: Optional[str] = None, llm_base_url: Optional[str] = None,
                 llm_model_name: Optional[str] = None):
        """
        Inicjalizacja detektora.
        
        Args:
            config: Konfiguracja anonimizacji.
            use_llm: Czy używać detektora LLM.
            llm_api_key: Klucz API do LLM (opcjonalny).
            llm_base_url: URL bazowy API LLM (opcjonalny).
            llm_model_name: Nazwa modelu LLM (opcjonalny).
        """
        self.config = config
        self.logger = logging.getLogger(__name__)
        self.use_llm = use_llm
        self.llm_api_key = llm_api_key
        self.llm_base_url = llm_base_url
        self.llm_model_name = llm_model_name
        
        # Lazy loading detektorów
        self._regex_detector = None
        self._nlp_detector = None
        self._polish_detector = None
        self._llm_detector = None
    
    @property
    def regex_detector(self):
        """Lazy loading detektora regex."""
        if self._regex_detector is None:
            from dane_bez_twarzy.detectors.regex_detector import RegexDetector
            self._regex_detector = RegexDetector(self.config)
        return self._regex_detector
    
    @property
    def nlp_detector(self):
        """Lazy loading detektora NLP."""
        if self._nlp_detector is None and self.config.use_nlp:
            try:
                from dane_bez_twarzy.detectors.nlp_detector import NLPDetector
                self._nlp_detector = NLPDetector(self.config)
            except ImportError:
                self.logger.warning("NLP detector niedostępny. Zainstaluj spaCy.")
        return self._nlp_detector
    
    @property
    def polish_detector(self):
        """Lazy loading detektora dla polskich wzorców."""
        if self._polish_detector is None and self.config.language == "pl":
            from dane_bez_twarzy.detectors.polish_detector import PolishDetector
            self._polish_detector = PolishDetector(self.config)
        return self._polish_detector
    
    @property
    def llm_detector(self):
        """Lazy loading detektora LLM."""
        if self._llm_detector is None and self.use_llm:
            try:
                from dane_bez_twarzy.detectors.llm_detector import LLMDetector
                self._llm_detector = LLMDetector(
                    self.config,
                    api_key=self.llm_api_key,
                    base_url=self.llm_base_url,
                    model_name=self.llm_model_name
                )
            except ImportError:
                self.logger.warning("LLM detector niedostępny. Zainstaluj langchain-openai.")
        return self._llm_detector
    
    def detect(self, text: str) -> List[Entity]:
        """
        Wykrywa wszystkie encje w tekście.
        
        Args:
            text: Tekst do analizy.
            
        Returns:
            Lista wykrytych encji.
        """
        if not text:
            return []
        
        entities = []
        
        # Wykrywanie przez regex (szybkie)
        entities.extend(self.regex_detector.detect(text))
        
        # Wykrywanie polskich wzorców
        if self.polish_detector:
            entities.extend(self.polish_detector.detect(text))
        
        # Wykrywanie przez NLP (wolniejsze, ale bardziej precyzyjne)
        if self.nlp_detector and self.config.use_nlp:
            entities.extend(self.nlp_detector.detect(text))
        
        # Wykrywanie przez LLM (bardzo dokładne, ale kosztowne)
        if self.llm_detector and self.use_llm:
            entities.extend(self.llm_detector.detect(text))
        
        # Usuń duplikaty i zachowaj te o wyższej pewności
        entities = self._deduplicate_entities(entities)
        
        # Filtruj po pewności
        entities = [
            e for e in entities 
            if e.confidence >= self.config.min_confidence
        ]
        
        # Filtruj po typach encji
        entities = [
            e for e in entities 
            if e.type in self.config.entities
        ]
        
        # Zastosuj wykluczenia
        if self.config.exclusions:
            entities = [
                e for e in entities
                if not self._is_excluded(e.text)
            ]
        
        # Sortuj po pozycji
        entities.sort(key=lambda e: e.start)
        
        return entities
    
    def _deduplicate_entities(self, entities: List[Entity]) -> List[Entity]:
        """
        Usuwa nakładające się encje, zachowując te o wyższej pewności.
        
        Args:
            entities: Lista encji do deduplikacji.
            
        Returns:
            Lista unikalnych encji.
        """
        if not entities:
            return []
        
        # Sortuj po pozycji i pewności
        entities.sort(key=lambda e: (e.start, -e.confidence))
        
        result = []
        last_end = -1
        
        for entity in entities:
            # Sprawdź czy encja się nie nakłada
            if entity.start >= last_end:
                result.append(entity)
                last_end = entity.end
            elif entity.confidence > result[-1].confidence:
                # Zastąp poprzednią encję, jeśli nowa ma wyższą pewność
                result[-1] = entity
                last_end = entity.end
        
        return result
    
    def _is_excluded(self, text: str) -> bool:
        """
        Sprawdza czy tekst jest na liście wykluczeń.
        
        Args:
            text: Tekst do sprawdzenia.
            
        Returns:
            True jeśli tekst powinien być wykluczony.
        """
        if not self.config.exclusions:
            return False
        
        text_lower = text.lower() if not self.config.case_sensitive else text
        
        for exclusion in self.config.exclusions:
            exclusion_cmp = exclusion.lower() if not self.config.case_sensitive else exclusion
            if exclusion_cmp in text_lower or text_lower in exclusion_cmp:
                return True
        
        return False
