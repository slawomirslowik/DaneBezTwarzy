"""
Wzorce regex dla wykrywania różnych typów danych.
"""

import re
from typing import Dict


class PolishPatterns:
    """Wzorce dla polskich danych osobowych."""
    
    # PESEL (11 cyfr)
    PESEL = re.compile(r'\b\d{11}\b')
    
    # NIP (10 cyfr z opcjonalnymi myślnikami)
    NIP = re.compile(r'\b\d{3}[-\s]?\d{3}[-\s]?\d{2}[-\s]?\d{2}\b|\b\d{10}\b')
    
    # REGON (9 lub 14 cyfr)
    REGON = re.compile(r'\b\d{9}\b|\b\d{14}\b')
    
    # Dowód osobisty (3 litery + 6 cyfr)
    ID_CARD = re.compile(r'\b[A-Z]{3}\s?\d{6}\b')
    
    # Paszport (2 litery + 7 cyfr)
    PASSPORT = re.compile(r'\b[A-Z]{2}\s?\d{7}\b')
    
    # Numer rejestracyjny pojazdu
    LICENSE_PLATE = re.compile(
        r'\b[A-Z]{2,3}\s?[A-Z0-9]{4,5}\b'  # Standard: ABC 12345
    )
    
    # Polski numer telefonu
    PHONE = re.compile(
        r'(?:\+48\s?)?(?:\d{3}[-\s]?\d{3}[-\s]?\d{3}|\d{2}[-\s]?\d{3}[-\s]?\d{2}[-\s]?\d{2}|\d{9})'
    )
    
    # Polski kod pocztowy
    POSTAL_CODE = re.compile(r'\b\d{2}-\d{3}\b')


class CommonPatterns:
    """Wzorce wspólne dla wielu języków."""
    
    # Email
    EMAIL = re.compile(
        r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    )
    
    # URL
    URL = re.compile(
        r'https?://(?:www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b(?:[-a-zA-Z0-9()@:%_\+.~#?&/=]*)'
    )
    
    # Adres IP (IPv4)
    IP_ADDRESS = re.compile(
        r'\b(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b'
    )
    
    # Numer karty kredytowej (podstawowy)
    CREDIT_CARD = re.compile(
        r'\b(?:\d{4}[-\s]?){3}\d{4}\b'
    )
    
    # Polski numer konta bankowego (26 cyfr z opcjonalnymi spacjami)
    BANK_ACCOUNT = re.compile(
        r'\b(?:\d{2}\s?)(?:\d{4}\s?){5}\d{4}\b'
    )
    
    # Data (różne formaty)
    DATE = re.compile(
        r'\b(?:\d{1,2}[-/\.]\d{1,2}[-/\.]\d{2,4}|\d{4}[-/\.]\d{1,2}[-/\.]\d{1,2})\b'
    )


class ValidationPatterns:
    """Wzorce do walidacji wykrytych danych."""
    
    @staticmethod
    def validate_pesel(pesel: str) -> bool:
        """
        Walidacja numeru PESEL (z checksumą).
        
        Args:
            pesel: Numer PESEL do walidacji.
            
        Returns:
            True jeśli PESEL jest poprawny.
        """
        if not pesel or len(pesel) != 11 or not pesel.isdigit():
            return False
        
        weights = [1, 3, 7, 9, 1, 3, 7, 9, 1, 3]
        checksum = sum(int(pesel[i]) * weights[i] for i in range(10)) % 10
        checksum = (10 - checksum) % 10
        
        return checksum == int(pesel[10])
    
    @staticmethod
    def validate_nip(nip: str) -> bool:
        """
        Walidacja numeru NIP (z checksumą).
        
        Args:
            nip: Numer NIP do walidacji.
            
        Returns:
            True jeśli NIP jest poprawny.
        """
        # Usuń myślniki i spacje
        nip = re.sub(r'[-\s]', '', nip)
        
        if not nip or len(nip) != 10 or not nip.isdigit():
            return False
        
        weights = [6, 5, 7, 2, 3, 4, 5, 6, 7]
        checksum = sum(int(nip[i]) * weights[i] for i in range(9)) % 11
        
        return checksum == int(nip[9])
    
    @staticmethod
    def validate_regon(regon: str) -> bool:
        """
        Walidacja numeru REGON.
        
        Args:
            regon: Numer REGON do walidacji.
            
        Returns:
            True jeśli REGON jest poprawny.
        """
        if not regon or len(regon) not in [9, 14] or not regon.isdigit():
            return False
        
        if len(regon) == 9:
            weights = [8, 9, 2, 3, 4, 5, 6, 7]
            checksum = sum(int(regon[i]) * weights[i] for i in range(8)) % 11
            checksum = 0 if checksum == 10 else checksum
            return checksum == int(regon[8])
        
        return True  # Uproszczona walidacja dla REGON-14
    
    @staticmethod
    def validate_credit_card(number: str) -> bool:
        """
        Walidacja numeru karty kredytowej (algorytm Luhna).
        
        Args:
            number: Numer karty do walidacji.
            
        Returns:
            True jeśli numer jest poprawny.
        """
        # Usuń spacje i myślniki
        number = re.sub(r'[-\s]', '', number)
        
        if not number or not number.isdigit() or len(number) < 13 or len(number) > 19:
            return False
        
        def luhn_checksum(card_number: str) -> bool:
            def digits_of(n: str):
                return [int(d) for d in n]
            
            digits = digits_of(card_number)
            odd_digits = digits[-1::-2]
            even_digits = digits[-2::-2]
            checksum = sum(odd_digits)
            
            for d in even_digits:
                checksum += sum(digits_of(str(d * 2)))
            
            return checksum % 10 == 0
        
        return luhn_checksum(number)


def get_patterns_for_entity_type(entity_type: str) -> Dict[str, re.Pattern]:
    """
    Zwraca wzorce regex dla danego typu encji.
    
    Args:
        entity_type: Typ encji (z EntityType enum).
        
    Returns:
        Słownik z wzorcami dla danego typu.
    """
    patterns_map = {
        "PESEL": {"pesel": PolishPatterns.PESEL},
        "NIP": {"nip": PolishPatterns.NIP},
        "REGON": {"regon": PolishPatterns.REGON},
        "ID_CARD": {"id_card": PolishPatterns.ID_CARD},
        "PASSPORT": {"passport": PolishPatterns.PASSPORT},
        "LICENSE_PLATE": {"license_plate": PolishPatterns.LICENSE_PLATE},
        "PHONE": {"phone": PolishPatterns.PHONE},
        "EMAIL": {"email": CommonPatterns.EMAIL},
        "URL": {"url": CommonPatterns.URL},
        "IP_ADDRESS": {"ip": CommonPatterns.IP_ADDRESS},
        "CREDIT_CARD": {"credit_card": CommonPatterns.CREDIT_CARD},
        "BANK_ACCOUNT": {"bank_account": CommonPatterns.BANK_ACCOUNT},
        "DATE_OF_BIRTH": {"date": CommonPatterns.DATE},
    }
    
    return patterns_map.get(entity_type, {})
