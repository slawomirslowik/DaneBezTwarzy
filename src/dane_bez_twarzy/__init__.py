"""
Dane Bez Twarzy - Biblioteka do anonimizacji danych osobowych.
"""

__version__ = "0.1.0"
__author__ = "Your Name"

from dane_bez_twarzy.core.anonymizer import Anonymizer
from dane_bez_twarzy.core.config import AnonymizationConfig, EntityType, AnonymizationMethod
from dane_bez_twarzy.core.detector import EntityDetector

__all__ = [
    "Anonymizer",
    "AnonymizationConfig",
    "EntityType",
    "AnonymizationMethod",
    "EntityDetector",
]
