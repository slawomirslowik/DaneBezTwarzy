"""
Strategie anonimizacji danych.
"""

from abc import ABC, abstractmethod
from typing import List
import hashlib
import secrets

from dane_bez_twarzy.core.config import AnonymizationConfig, AnonymizationMethod
from dane_bez_twarzy.core.detector import Entity


class AnonymizationStrategy(ABC):
    """Bazowa klasa dla strategii anonimizacji."""
    
    def __init__(self, config: AnonymizationConfig):
        """
        Inicjalizacja strategii.
        
        Args:
            config: Konfiguracja anonimizacji.
        """
        self.config = config
    
    @abstractmethod
    def anonymize(self, text: str, entities: List[Entity]) -> str:
        """
        Anonimizuje tekst na podstawie wykrytych encji.
        
        Args:
            text: Oryginalny tekst.
            entities: Lista wykrytych encji.
            
        Returns:
            Zanonimizowany tekst.
        """
        pass
    
    def _replace_entities(self, text: str, entities: List[Entity], replacements: dict) -> str:
        """
        Pomocnicza metoda do zamiany encji w tekście.
        
        Args:
            text: Oryginalny tekst.
            entities: Lista encji do zamiany.
            replacements: Słownik mapowania encji na ich zamienniki.
            
        Returns:
            Tekst z zamienionymi encjami.
        """
        # Sortuj encje od końca do początku, żeby nie psuć indeksów
        sorted_entities = sorted(entities, key=lambda e: e.start, reverse=True)
        
        result = text
        for entity in sorted_entities:
            replacement = replacements.get(entity.text, entity.text)
            result = result[:entity.start] + replacement + result[entity.end:]
        
        return result


class MaskStrategy(AnonymizationStrategy):
    """Strategia maskowania - zamienia znaki na maskę."""
    
    def anonymize(self, text: str, entities: List[Entity]) -> str:
        """Maskuje wykryte encje."""
        replacements = {}
        
        for entity in entities:
            if self.config.preserve_length:
                # Zachowaj długość i strukturę
                if self.config.preserve_structure:
                    masked = self._mask_with_structure(entity.text)
                else:
                    masked = self.config.mask_char * len(entity.text)
            else:
                # Stała długość maski
                masked = self.config.mask_char * 3
            
            replacements[entity.text] = masked
        
        return self._replace_entities(text, entities, replacements)
    
    def _mask_with_structure(self, text: str) -> str:
        """Maskuje zachowując strukturę (spacje, myślniki, itp.)."""
        result = []
        for char in text:
            if char.isalnum():
                result.append(self.config.mask_char)
            else:
                result.append(char)
        return ''.join(result)


class PseudonymizeStrategy(AnonymizationStrategy):
    """Strategia pseudonimizacji - zamienia na konsystentne pseudonimy."""
    
    def __init__(self, config: AnonymizationConfig):
        super().__init__(config)
        self._pseudonym_map = {}
        self._counter = {}
        
        # Ustaw seed dla powtarzalności
        if config.seed:
            import random
            random.seed(config.seed)
    
    def anonymize(self, text: str, entities: List[Entity]) -> str:
        """Pseudonimizuje wykryte encje."""
        replacements = {}
        
        for entity in entities:
            if entity.text not in self._pseudonym_map:
                # Wygeneruj nowy pseudonim
                entity_type_str = entity.type.value
                if entity_type_str not in self._counter:
                    self._counter[entity_type_str] = 0
                
                self._counter[entity_type_str] += 1
                pseudonym = f"[{entity_type_str}_{self._counter[entity_type_str]}]"
                
                self._pseudonym_map[entity.text] = pseudonym
            
            replacements[entity.text] = self._pseudonym_map[entity.text]
        
        return self._replace_entities(text, entities, replacements)


class HashStrategy(AnonymizationStrategy):
    """Strategia haszowania - nieodwracalna anonimizacja."""
    
    def anonymize(self, text: str, entities: List[Entity]) -> str:
        """Haszuje wykryte encje."""
        replacements = {}
        
        for entity in entities:
            hashed = self._hash_text(entity.text)
            replacements[entity.text] = hashed
        
        return self._replace_entities(text, entities, replacements)
    
    def _hash_text(self, text: str) -> str:
        """Haszuje tekst."""
        # Dodaj salt jeśli jest skonfigurowany
        data = text
        if self.config.hash_salt:
            data = self.config.hash_salt + text
        
        # Użyj wybranego algorytmu
        if self.config.hash_algorithm == "sha256":
            hash_obj = hashlib.sha256(data.encode())
        elif self.config.hash_algorithm == "sha512":
            hash_obj = hashlib.sha512(data.encode())
        elif self.config.hash_algorithm == "md5":
            hash_obj = hashlib.md5(data.encode())
        else:
            hash_obj = hashlib.sha256(data.encode())
        
        # Zwróć skrócony hash (pierwsze 16 znaków)
        return hash_obj.hexdigest()[:16]


class RedactStrategy(AnonymizationStrategy):
    """Strategia usuwania - całkowite usunięcie danych."""
    
    def anonymize(self, text: str, entities: List[Entity]) -> str:
        """Usuwa wykryte encje."""
        replacements = {}
        
        for entity in entities:
            replacements[entity.text] = "[USUNIĘTO]"
        
        return self._replace_entities(text, entities, replacements)


class GeneralizeStrategy(AnonymizationStrategy):
    """Strategia generalizacji - zamienia na ogólniejsze wartości."""
    
    def anonymize(self, text: str, entities: List[Entity]) -> str:
        """Generalizuje wykryte encje."""
        replacements = {}
        
        for entity in entities:
            generalized = self._generalize(entity)
            replacements[entity.text] = generalized
        
        return self._replace_entities(text, entities, replacements)
    
    def _generalize(self, entity: Entity) -> str:
        """Generalizuje encję do ogólniejszej formy."""
        from dane_bez_twarzy.core.config import EntityType
        
        # Mapowanie typów na ogólne wartości
        generalizations = {
            EntityType.PERSON: "[OSOBA]",
            EntityType.EMAIL: "[EMAIL]",
            EntityType.PHONE: "[TELEFON]",
            EntityType.PESEL: "[PESEL]",
            EntityType.ADDRESS: "[ADRES]",
            EntityType.BANK_ACCOUNT: "[KONTO BANKOWE]",
            EntityType.CREDIT_CARD: "[KARTA]",
            EntityType.DATE_OF_BIRTH: "[DATA]",
        }
        
        return generalizations.get(entity.type, "[DANE OSOBOWE]")


class EncryptStrategy(AnonymizationStrategy):
    """Strategia szyfrowania - odwracalna anonimizacja."""
    
    def anonymize(self, text: str, entities: List[Entity]) -> str:
        """Szyfruje wykryte encje."""
        replacements = {}
        
        for entity in entities:
            encrypted = self._encrypt(entity.text)
            replacements[entity.text] = encrypted
        
        return self._replace_entities(text, entities, replacements)
    
    def _encrypt(self, text: str) -> str:
        """Szyfruje tekst."""
        try:
            from cryptography.fernet import Fernet
            
            # Użyj klucza z konfiguracji lub wygeneruj nowy
            key = self.config.encryption_key
            if not key:
                key = Fernet.generate_key().decode()
            
            if isinstance(key, str):
                key = key.encode()
            
            f = Fernet(key)
            encrypted = f.encrypt(text.encode())
            
            # Zwróć jako hex dla czytelności
            return f"[ENC:{encrypted.hex()[:32]}...]"
        
        except ImportError:
            return "[ZASZYFROWANO]"
    
    def decrypt(self, encrypted_text: str) -> str:
        """Odszyfrowuje tekst (wymaga oryginalnego klucza)."""
        # Implementacja deszyfrowania
        raise NotImplementedError("Deszyfrowanie będzie dodane w przyszłej wersji")


def get_strategy(method: AnonymizationMethod, config: AnonymizationConfig) -> AnonymizationStrategy:
    """
    Zwraca odpowiednią strategię anonimizacji.
    
    Args:
        method: Metoda anonimizacji.
        config: Konfiguracja.
        
    Returns:
        Instancja strategii.
    """
    strategies = {
        AnonymizationMethod.MASK: MaskStrategy,
        AnonymizationMethod.PSEUDONYMIZE: PseudonymizeStrategy,
        AnonymizationMethod.HASH: HashStrategy,
        AnonymizationMethod.REDACT: RedactStrategy,
        AnonymizationMethod.GENERALIZE: GeneralizeStrategy,
        AnonymizationMethod.ENCRYPT: EncryptStrategy,
    }
    
    strategy_class = strategies.get(method)
    if not strategy_class:
        raise ValueError(f"Nieznana metoda anonimizacji: {method}")
    
    return strategy_class(config)
