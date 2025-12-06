"""
Testy dla modułu konfiguracji.
"""

import pytest
from dane_bez_twarzy.core.config import (
    AnonymizationConfig,
    EntityType,
    AnonymizationMethod
)


def test_default_config():
    """Test domyślnej konfiguracji."""
    config = AnonymizationConfig()
    
    assert config.language == "pl"
    assert config.method == AnonymizationMethod.MASK
    assert config.mask_char == "*"
    assert config.preserve_length is True
    assert len(config.entities) > 0


def test_custom_config():
    """Test własnej konfiguracji."""
    config = AnonymizationConfig(
        language="en",
        method="pseudonymize",
        entities=[EntityType.PERSON, EntityType.EMAIL]
    )
    
    assert config.language == "en"
    assert config.method == AnonymizationMethod.PSEUDONYMIZE
    assert len(config.entities) == 2


def test_config_validation():
    """Test walidacji konfiguracji."""
    # Nieprawidłowa pewność
    with pytest.raises(ValueError):
        AnonymizationConfig(min_confidence=1.5)
    
    # Brak klucza dla szyfrowania
    with pytest.raises(ValueError):
        AnonymizationConfig(method="encrypt")


def test_string_to_enum_conversion():
    """Test konwersji stringów na enumy."""
    config = AnonymizationConfig(
        method="mask",
        entities=["PERSON", "EMAIL"]
    )
    
    assert isinstance(config.method, AnonymizationMethod)
    assert all(isinstance(e, EntityType) for e in config.entities)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
