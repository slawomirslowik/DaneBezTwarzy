"""
Detektor używający modelu językowego PLLUM do wykrywania encji.
"""

from typing import List, Optional
import logging
import json
import re

from dane_bez_twarzy.core.config import AnonymizationConfig, EntityType
from dane_bez_twarzy.core.detector import Entity


class LLMDetector:
    """
    Wykrywa encje używając modelu językowego PLLUM.
    Model analizuje tekst kontekstowo i rozpoznaje różne typy danych wrażliwych.
    """
    
    def __init__(self, config: AnonymizationConfig, api_key: Optional[str] = None, 
                 base_url: Optional[str] = None, model_name: Optional[str] = None):
        """
        Inicjalizacja detektora LLM.
        
        Args:
            config: Konfiguracja anonimizacji.
            api_key: Klucz API do PLLUM (Ocp-Apim-Subscription-Key).
            base_url: URL bazowy API.
            model_name: Nazwa modelu do użycia.
        """
        self.config = config
        self.logger = logging.getLogger(__name__)
        
        # Konfiguracja LLM
        self.api_key = api_key or "c670f40b37e0495c845c63b1e548d95a"
        self.base_url = base_url or "https://apim-pllum-tst-pcn.azure-api.net/vllm/v1"
        self.model_name = model_name or "CYFRAGOVPL/pllum-12b-nc-chat-250715"
        
        self.llm = None
        self._load_llm()
    
    def _load_llm(self) -> None:
        """Inicjalizuje połączenie z LLM."""
        try:
            from langchain_openai import ChatOpenAI
            
            self.llm = ChatOpenAI(
                model=self.model_name,
                openai_api_key="EMPTY",
                openai_api_base=self.base_url,
                temperature=0.1,  # Niska temperatura dla deterministycznych wyników
                max_tokens=2000,
                default_headers={
                    'Ocp-Apim-Subscription-Key': self.api_key
                }
            )
            self.logger.info(f"Załadowano model LLM: {self.model_name}")
            
        except ImportError:
            self.logger.error(
                "Biblioteka langchain_openai nie jest zainstalowana. "
                "Zainstaluj: pip install langchain-openai"
            )
            raise
        except Exception as e:
            self.logger.error(f"Błąd podczas inicjalizacji LLM: {e}")
            raise
    
    def detect(self, text: str) -> List[Entity]:
        """
        Wykrywa encje w tekście używając LLM.
        
        Args:
            text: Tekst do analizy.
            
        Returns:
            Lista wykrytych encji.
        """
        if not text or not self.llm:
            return []
        
        try:
            # Przygotuj prompt dla modelu
            prompt = self._create_detection_prompt(text)
            
            # Wywołaj model
            response = self.llm.invoke(prompt)
            
            # Parsuj odpowiedź
            entities = self._parse_llm_response(response, text)
            
            self.logger.info(f"LLM wykrył {len(entities)} encji")
            return entities
            
        except Exception as e:
            self.logger.error(f"Błąd podczas wykrywania encji przez LLM: {e}")
            return []
    
    def _create_detection_prompt(self, text: str) -> str:
        """
        Tworzy prompt dla modelu do wykrywania encji.
        
        Args:
            text: Tekst do analizy.
            
        Returns:
            Prompt dla modelu.
        """
        # Mapowanie typów encji na opis w języku polskim
        entity_descriptions = {
            EntityType.PERSON: "imiona i nazwiska osób",
            EntityType.EMAIL: "adresy email",
            EntityType.PHONE: "numery telefonu",
            EntityType.PESEL: "numery PESEL",
            EntityType.NIP: "numery NIP",
            EntityType.REGON: "numery REGON",
            EntityType.ADDRESS: "adresy (ulice, miasta, kody pocztowe)",
            EntityType.CREDIT_CARD: "numery kart kredytowych",
            EntityType.IBAN: "numery kont bankowych IBAN",
            EntityType.ID_CARD: "numery dowodów osobistych",
            EntityType.PASSPORT: "numery paszportów",
            EntityType.ORGANIZATION: "nazwy organizacji i firm",
            EntityType.DATE: "daty urodzenia i inne wrażliwe daty"
        }
        
        # Filtruj tylko te typy encji, które są w konfiguracji
        requested_types = [
            entity_descriptions.get(entity_type, entity_type.value)
            for entity_type in self.config.entities
            if entity_type in entity_descriptions
        ]
        
        entity_list = ", ".join(requested_types)
        
        prompt = f"""Jesteś ekspertem w wykrywaniu danych wrażliwych w tekstach.
Przeanalizuj poniższy tekst i znajdź wszystkie dane osobowe i wrażliwe, takie jak: {entity_list}.

TEKST DO ANALIZY:
{text}

INSTRUKCJE:
1. Znajdź wszystkie wystąpienia danych wrażliwych w tekście
2. Dla każdej znalezionej danej podaj:
   - typ (np. PERSON, EMAIL, PHONE, PESEL, NIP, ADDRESS, itp.)
   - dokładny tekst, który występuje w tekście
   - pozycję początkową i końcową w tekście (indeksy znaków)
   - poziom pewności (0.0-1.0)

WAŻNE: Zwróć wynik w formacie JSON jako listę obiektów:
[
  {{"type": "PERSON", "text": "Jan Kowalski", "start": 10, "end": 23, "confidence": 0.95}},
  {{"type": "EMAIL", "text": "jan@example.com", "start": 45, "end": 60, "confidence": 1.0}}
]

Jeśli nie znajdziesz żadnych danych wrażliwych, zwróć pustą listę: []

ODPOWIEDŹ (tylko JSON, bez dodatkowych komentarzy):"""
        
        return prompt
    
    def _parse_llm_response(self, response, original_text: str) -> List[Entity]:
        """
        Parsuje odpowiedź z LLM i tworzy listę encji.
        
        Args:
            response: Odpowiedź z modelu LLM.
            original_text: Oryginalny tekst do analizy.
            
        Returns:
            Lista wykrytych encji.
        """
        entities = []
        
        try:
            # Wyciągnij treść odpowiedzi
            if hasattr(response, 'content'):
                response_text = response.content
            elif hasattr(response, 'json'):
                response_json = response.json()
                response_text = response_json.get('choices', [{}])[0].get('message', {}).get('content', '')
            else:
                response_text = str(response)
            
            # Znajdź JSON w odpowiedzi (może być otoczony markdown lub tekstem)
            json_match = re.search(r'\[.*\]', response_text, re.DOTALL)
            if not json_match:
                self.logger.warning("Nie znaleziono JSON w odpowiedzi LLM")
                return []
            
            json_text = json_match.group(0)
            detected_entities = json.loads(json_text)
            
            # Konwertuj na obiekty Entity
            for entity_data in detected_entities:
                try:
                    entity_type_str = entity_data.get('type', '').upper()
                    
                    # Mapuj typ z odpowiedzi na EntityType
                    try:
                        entity_type = EntityType[entity_type_str]
                    except KeyError:
                        # Spróbuj zmapować na najbliższy typ
                        entity_type = self._map_to_entity_type(entity_type_str)
                        if not entity_type:
                            continue
                    
                    # Waliduj czy tekst faktycznie występuje w podanej pozycji
                    text = entity_data.get('text', '')
                    start = entity_data.get('start', 0)
                    end = entity_data.get('end', start + len(text))
                    
                    # Jeśli pozycje są niepoprawne, spróbuj znaleźć tekst
                    if start >= len(original_text) or original_text[start:end] != text:
                        start = original_text.find(text)
                        if start == -1:
                            continue
                        end = start + len(text)
                    
                    entity = Entity(
                        text=text,
                        type=entity_type,
                        start=start,
                        end=end,
                        confidence=float(entity_data.get('confidence', 0.8)),
                        metadata={'source': 'llm', 'model': self.model_name}
                    )
                    
                    entities.append(entity)
                    
                except (KeyError, ValueError, TypeError) as e:
                    self.logger.warning(f"Błąd podczas parsowania encji: {e}, dane: {entity_data}")
                    continue
            
        except json.JSONDecodeError as e:
            self.logger.error(f"Błąd podczas parsowania JSON z LLM: {e}")
        except Exception as e:
            self.logger.error(f"Nieoczekiwany błąd podczas parsowania odpowiedzi LLM: {e}")
        
        return entities
    
    def _map_to_entity_type(self, type_str: str) -> Optional[EntityType]:
        """
        Mapuje string na EntityType.
        
        Args:
            type_str: String reprezentujący typ encji.
            
        Returns:
            EntityType lub None jeśli nie można zmapować.
        """
        # Mapowanie alternatywnych nazw
        mapping = {
            'NAME': EntityType.PERSON,
            'NAZWISKO': EntityType.PERSON,
            'IMIE': EntityType.PERSON,
            'TELEFON': EntityType.PHONE,
            'MAIL': EntityType.EMAIL,
            'ADRES': EntityType.ADDRESS,
            'KARTA': EntityType.CREDIT_CARD,
            'DOWOD': EntityType.ID_CARD,
            'PASZPORT': EntityType.PASSPORT,
            'FIRMA': EntityType.ORGANIZATION,
            'DATA': EntityType.DATE,
        }
        
        type_str_upper = type_str.upper()
        
        # Sprawdź bezpośrednie mapowanie
        if type_str_upper in mapping:
            return mapping[type_str_upper]
        
        # Sprawdź czy zawiera słowo kluczowe
        for key, value in mapping.items():
            if key in type_str_upper:
                return value
        
        return None
