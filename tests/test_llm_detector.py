"""
Testy dla detektora LLM.
"""

import pytest
from unittest.mock import Mock, patch

from dane_bez_twarzy.detectors.llm_detector import LLMDetector
from dane_bez_twarzy.core.config import AnonymizationConfig, EntityType
from dane_bez_twarzy.core.detector import Entity


@pytest.fixture
def config():
    """Podstawowa konfiguracja."""
    return AnonymizationConfig(
        entities=[EntityType.PERSON, EntityType.EMAIL, EntityType.PHONE],
        language="pl"
    )


@pytest.fixture
def mock_llm():
    """Mock dla modelu LLM."""
    mock = Mock()
    mock_response = Mock()
    mock_response.content = '''[
        {"type": "PERSON", "text": "Jan Kowalski", "start": 0, "end": 13, "confidence": 0.95},
        {"type": "EMAIL", "text": "jan@example.com", "start": 20, "end": 35, "confidence": 1.0}
    ]'''
    mock.invoke.return_value = mock_response
    return mock


class TestLLMDetector:
    """Testy dla klasy LLMDetector."""
    
    @patch('dane_bez_twarzy.detectors.llm_detector.ChatOpenAI')
    def test_init(self, mock_chat_openai, config):
        """Test inicjalizacji detektora."""
        detector = LLMDetector(
            config,
            api_key="test_key",
            base_url="http://test.com",
            model_name="test_model"
        )
        
        assert detector.config == config
        assert detector.api_key == "test_key"
        assert detector.base_url == "http://test.com"
        assert detector.model_name == "test_model"
        mock_chat_openai.assert_called_once()
    
    @patch('dane_bez_twarzy.detectors.llm_detector.ChatOpenAI')
    def test_detect_with_mock(self, mock_chat_openai, config, mock_llm):
        """Test wykrywania encji z mock LLM."""
        mock_chat_openai.return_value = mock_llm
        
        detector = LLMDetector(config)
        text = "Jan Kowalski, email: jan@example.com"
        
        entities = detector.detect(text)
        
        assert len(entities) == 2
        assert entities[0].text == "Jan Kowalski"
        assert entities[0].type == EntityType.PERSON
        assert entities[1].text == "jan@example.com"
        assert entities[1].type == EntityType.EMAIL
    
    def test_create_detection_prompt(self, config):
        """Test tworzenia promptu."""
        with patch('dane_bez_twarzy.detectors.llm_detector.ChatOpenAI'):
            detector = LLMDetector(config)
            
            text = "Test text"
            prompt = detector._create_detection_prompt(text)
            
            assert "Test text" in prompt
            assert "JSON" in prompt
            assert "PERSON" in prompt or "imiona" in prompt
    
    def test_map_to_entity_type(self, config):
        """Test mapowania typów encji."""
        with patch('dane_bez_twarzy.detectors.llm_detector.ChatOpenAI'):
            detector = LLMDetector(config)
            
            assert detector._map_to_entity_type("NAME") == EntityType.PERSON
            assert detector._map_to_entity_type("NAZWISKO") == EntityType.PERSON
            assert detector._map_to_entity_type("TELEFON") == EntityType.PHONE
            assert detector._map_to_entity_type("MAIL") == EntityType.EMAIL
            assert detector._map_to_entity_type("UNKNOWN") is None
    
    @patch('dane_bez_twarzy.detectors.llm_detector.ChatOpenAI')
    def test_detect_empty_text(self, mock_chat_openai, config):
        """Test wykrywania w pustym tekście."""
        detector = LLMDetector(config)
        
        entities = detector.detect("")
        assert entities == []
        
        entities = detector.detect(None)
        assert entities == []
    
    @patch('dane_bez_twarzy.detectors.llm_detector.ChatOpenAI')
    def test_parse_llm_response_invalid_json(self, mock_chat_openai, config, mock_llm):
        """Test parsowania niepoprawnej odpowiedzi JSON."""
        mock_llm.invoke.return_value.content = "Invalid JSON response"
        mock_chat_openai.return_value = mock_llm
        
        detector = LLMDetector(config)
        entities = detector.detect("Test text")
        
        assert entities == []
    
    @patch('dane_bez_twarzy.detectors.llm_detector.ChatOpenAI')
    def test_detect_with_invalid_positions(self, mock_chat_openai, config, mock_llm):
        """Test wykrywania z nieprawidłowymi pozycjami."""
        # Odpowiedź z błędnymi pozycjami
        mock_llm.invoke.return_value.content = '''[
            {"type": "PERSON", "text": "Jan Kowalski", "start": 1000, "end": 1013, "confidence": 0.95}
        ]'''
        mock_chat_openai.return_value = mock_llm
        
        detector = LLMDetector(config)
        text = "Jan Kowalski"
        entities = detector.detect(text)
        
        # Powinien znaleźć tekst i poprawić pozycje
        assert len(entities) == 1
        assert entities[0].text == "Jan Kowalski"
        assert entities[0].start == 0
        assert entities[0].end == 13


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
