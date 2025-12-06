"""
Główny moduł anonimizacji danych.
"""

import logging
from pathlib import Path
from typing import Union, List, Optional, Dict, Any

from dane_bez_twarzy.core.config import AnonymizationConfig
from dane_bez_twarzy.core.detector import EntityDetector
from dane_bez_twarzy.strategies import get_strategy
from dane_bez_twarzy.processors import get_processor
from dane_bez_twarzy.utils.logger import setup_logger


class Anonymizer:
    """
    Główna klasa do anonimizacji danych.
    
    Przykład użycia:
        >>> config = AnonymizationConfig(language="pl", method="mask")
        >>> anonymizer = Anonymizer(config)
        >>> result = anonymizer.anonymize_text("Jan Kowalski, tel: 123-456-789")
        >>> print(result)
        '*** ********, tel: ***********'
    """
    
    def __init__(self, config: Optional[AnonymizationConfig] = None, 
                 use_llm: bool = False, llm_api_key: Optional[str] = None,
                 llm_base_url: Optional[str] = None, llm_model_name: Optional[str] = None):
        """
        Inicjalizacja anonimizera.
        
        Args:
            config: Konfiguracja anonimizacji. Jeśli None, użyje domyślnej.
            use_llm: Czy używać detektora LLM.
            llm_api_key: Klucz API do LLM (opcjonalny).
            llm_base_url: URL bazowy API LLM (opcjonalny).
            llm_model_name: Nazwa modelu LLM (opcjonalny).
        """
        self.config = config or AnonymizationConfig()
        self.logger = setup_logger(
            level=self.config.log_level,
            verbose=self.config.verbose
        )
        
        # Przechowywanie informacji o aktualnie przetwarzanym pliku
        self._current_file = None
        
        # Inicjalizacja detektora encji
        self.detector = EntityDetector(
            self.config,
            use_llm=use_llm,
            llm_api_key=llm_api_key,
            llm_base_url=llm_base_url,
            llm_model_name=llm_model_name
        )
        
        # Inicjalizacja strategii anonimizacji
        self.strategy = get_strategy(self.config.method, self.config)
        
        self.logger.info(f"Anonimizer zainicjalizowany: metoda={self.config.method.value}")
        if use_llm:
            self.logger.info("Detektor LLM włączony")
    
    def anonymize_text(self, text: str, log_prefix: str = "") -> str:
        """
        Anonimizuje tekst.
        
        Args:
            text: Tekst do anonimizacji.
            log_prefix: Prefiks dla logów (np. nazwa pliku).
            
        Returns:
            Zanonimizowany tekst.
        """
        if not text:
            return text
        
        # Wykryj encje
        entities = self.detector.detect(text)
        
        if not entities:
            self.logger.debug("Nie znaleziono encji do anonimizacji")
            return text
        
        self.logger.info(f"Znaleziono {len(entities)} encji do anonimizacji")
        
        # Loguj szczegóły każdej zanonimizowanej encji
        self._log_entity_details(text, entities, log_prefix)
        
        # Anonimizuj tekst
        anonymized_text = self.strategy.anonymize(text, entities)
        
        return anonymized_text
    
    def _log_entity_details(self, text: str, entities: List, log_prefix: str = "") -> None:
        """
        Loguje szczegółowe informacje o wykrytych encjach.
        
        Args:
            text: Oryginalny tekst.
            entities: Lista wykrytych encji.
            log_prefix: Prefiks dla logów.
        """
        if not self.config.verbose:
            return
        
        # Dodaj nazwę pliku do prefiksu jeśli dostępna
        if self._current_file and not log_prefix:
            log_prefix = f"[{self._current_file}] "
        
        # Oblicz numery linii i kolumn dla każdej encji
        for entity in entities:
            line_num, col_num = self._get_position(text, entity.start)
            
            detector_info = entity.metadata.get('detector', 'unknown') if entity.metadata else 'unknown'
            
            log_msg = (
                f"{log_prefix}Zanonimizowano: "
                f"typ={entity.type.value}, "
                f"tekst='{entity.text}', "
                f"linia={line_num}, "
                f"kolumna={col_num}, "
                f"pozycja={entity.start}-{entity.end}, "
                f"pewność={entity.confidence:.2f}, "
                f"detektor={detector_info}"
            )
            
            self.logger.info(log_msg)
    
    def _get_position(self, text: str, offset: int) -> tuple:
        """
        Oblicza numer linii i kolumny na podstawie offsetu w tekście.
        
        Args:
            text: Tekst źródłowy.
            offset: Pozycja znaku (offset).
            
        Returns:
            Tuple (numer_linii, numer_kolumny) - numeracja od 1.
        """
        lines = text[:offset].split('\n')
        line_num = len(lines)
        col_num = len(lines[-1]) + 1 if lines else 1
        return line_num, col_num
    
    def anonymize_file(
        self,
        input_path: Union[str, Path],
        output_path: Optional[Union[str, Path]] = None,
        **kwargs: Any
    ) -> Path:
        """
        Anonimizuje plik.
        
        Args:
            input_path: Ścieżka do pliku wejściowego.
            output_path: Ścieżka do pliku wyjściowego. Jeśli None, użyje nazwy z sufiksem.
            **kwargs: Dodatkowe argumenty dla processora.
            
        Returns:
            Ścieżka do zanonimizowanego pliku.
        """
        input_path = Path(input_path)
        
        if not input_path.exists():
            raise FileNotFoundError(f"Plik nie istnieje: {input_path}")
        
        # Określ ścieżkę wyjściową
        if output_path is None:
            output_path = input_path.parent / f"{input_path.stem}_anonimizowany{input_path.suffix}"
        else:
            output_path = Path(output_path)
        
        self.logger.info(f"Anonimizacja pliku: {input_path} -> {output_path}")
        
        # Pobierz odpowiedni processor
        processor = get_processor(input_path.suffix)
        
        # Zapisz nazwę pliku dla logowania
        self._current_file = str(input_path.name)
        
        # Przetwórz plik
        processor.process(
            input_path=input_path,
            output_path=output_path,
            anonymizer=self,
            **kwargs
        )
        
        self._current_file = None
        
        self.logger.info(f"Plik zanonimizowany: {output_path}")
        return output_path
    
    def anonymize_directory(
        self,
        input_dir: Union[str, Path],
        output_dir: Union[str, Path],
        recursive: bool = True,
        file_patterns: Optional[List[str]] = None,
        **kwargs: Any
    ) -> List[Path]:
        """
        Anonimizuje wszystkie pliki w katalogu.
        
        Args:
            input_dir: Katalog wejściowy.
            output_dir: Katalog wyjściowy.
            recursive: Czy przetwarzać rekurencyjnie.
            file_patterns: Lista wzorców plików (np. ["*.txt", "*.docx"]).
            **kwargs: Dodatkowe argumenty dla processorów.
            
        Returns:
            Lista ścieżek do zanonimizowanych plików.
        """
        input_dir = Path(input_dir)
        output_dir = Path(output_dir)
        
        if not input_dir.exists():
            raise FileNotFoundError(f"Katalog nie istnieje: {input_dir}")
        
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Domyślne wzorce
        if file_patterns is None:
            file_patterns = ["*.txt", "*.docx", "*.xlsx", "*.pdf", "*.csv"]
        
        # Zbierz pliki
        files = []
        for pattern in file_patterns:
            if recursive:
                files.extend(input_dir.rglob(pattern))
            else:
                files.extend(input_dir.glob(pattern))
        
        self.logger.info(f"Znaleziono {len(files)} plików do przetworzenia")
        
        # Przetwórz pliki
        results = []
        for file_path in files:
            try:
                # Zachowaj strukturę katalogów
                relative_path = file_path.relative_to(input_dir)
                output_path = output_dir / relative_path
                output_path.parent.mkdir(parents=True, exist_ok=True)
                
                result = self.anonymize_file(file_path, output_path, **kwargs)
                results.append(result)
                
            except Exception as e:
                self.logger.error(f"Błąd podczas przetwarzania {file_path}: {e}")
                continue
        
        self.logger.info(f"Przetworzono {len(results)}/{len(files)} plików")
        return results
    
    def detect_entities(self, text: str) -> List[Dict[str, Any]]:
        """
        Wykrywa encje w tekście bez anonimizacji (tryb analizy).
        
        Args:
            text: Tekst do analizy.
            
        Returns:
            Lista wykrytych encji z informacjami.
        """
        entities = self.detector.detect(text)
        return [
            {
                "text": entity.text,
                "type": entity.type.value,
                "start": entity.start,
                "end": entity.end,
                "confidence": entity.confidence
            }
            for entity in entities
        ]
    
    def generate_report(self, text: str, output_path: Optional[Union[str, Path]] = None) -> Dict[str, Any]:
        """
        Generuje raport z analizy tekstu.
        
        Args:
            text: Tekst do analizy.
            output_path: Opcjonalna ścieżka do zapisu raportu.
            
        Returns:
            Słownik z raportem.
        """
        entities = self.detect_entities(text)
        
        # Statystyki
        stats = {}
        for entity in entities:
            entity_type = entity["type"]
            stats[entity_type] = stats.get(entity_type, 0) + 1
        
        report = {
            "total_entities": len(entities),
            "entities_by_type": stats,
            "entities": entities,
            "config": {
                "method": self.config.method.value,
                "language": self.config.language,
                "min_confidence": self.config.min_confidence
            }
        }
        
        # Zapis do pliku
        if output_path:
            import json
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(report, f, indent=2, ensure_ascii=False)
            self.logger.info(f"Raport zapisany: {output_path}")
        
        return report
