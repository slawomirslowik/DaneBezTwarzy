"""
Detektor NLP/NER używający spaCy.
"""

from typing import List, Optional
import logging

from dane_bez_twarzy.core.config import AnonymizationConfig, EntityType
from dane_bez_twarzy.core.detector import Entity


class NLPDetector:
    """
    Wykrywa encje używając NLP (Named Entity Recognition).
    Używa biblioteki spaCy do analizy kontekstowej.
    """
    
    def __init__(self, config: AnonymizationConfig):
        """
        Inicjalizacja detektora NLP.
        
        Args:
            config: Konfiguracja anonimizacji.
        """
        self.config = config
        self.logger = logging.getLogger(__name__)
        self.nlp = None
        
        # Lazy loading modelu spaCy
        self._load_model()
    
    def _load_model(self) -> None:
        """Ładuje model spaCy."""
        try:
            import spacy
            
            model_name = self.config.nlp_model
            
            try:
                self.nlp = spacy.load(model_name)
                self.logger.info(f"Załadowano model spaCy: {model_name}")
            except OSError:
                self.logger.warning(
                    f"Model {model_name} nie jest zainstalowany. "
                    f"Uruchom: python -m spacy download {model_name}"
                )
                # Fallback na mniejszy model
                try:
                    self.nlp = spacy.load("pl_core_news_sm")
                    self.logger.info("Użyto mniejszego modelu: pl_core_news_sm")
                except OSError:
                    self.logger.error("Brak dostępnych modeli spaCy dla języka polskiego")
        
        except ImportError:
            self.logger.error("spaCy nie jest zainstalowane. Zainstaluj: pip install spacy")
    
    def detect(self, text: str) -> List[Entity]:
        """
        Wykrywa encje używając NLP.
        
        Args:
            text: Tekst do analizy.
            
        Returns:
            Lista wykrytych encji.
        """
        if not self.nlp:
            return []
        
        entities = []
        
        # Przetwórz tekst przez spaCy
        doc = self.nlp(text)
        
        # Mapowanie typów spaCy na nasze typy
        spacy_to_entity_type = {
            "PER": EntityType.PERSON,
            "PERSON": EntityType.PERSON,
            "ORG": EntityType.ORGANIZATION,
            "LOC": EntityType.LOCATION,
            "GPE": EntityType.LOCATION,
        }
        
        # Wykryj nazwane encje
        for ent in doc.ents:
            entity_type = spacy_to_entity_type.get(ent.label_)
            
            if entity_type and entity_type in self.config.entities:
                entity = Entity(
                    text=ent.text,
                    type=entity_type,
                    start=ent.start_char,
                    end=ent.end_char,
                    confidence=0.85,  # spaCy nie zwraca confidence dla wszystkich modeli
                    metadata={
                        "detector": "nlp",
                        "spacy_label": ent.label_
                    }
                )
                entities.append(entity)
        
        return entities
