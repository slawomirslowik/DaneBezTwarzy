"""
Logger setup for the library.
"""

import logging
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Optional

try:
    import colorlog
    COLORLOG_AVAILABLE = True
except ImportError:
    COLORLOG_AVAILABLE = False


def setup_logger(
    name: str = "dane_bez_twarzy",
    level: str = "INFO",
    verbose: bool = False
) -> logging.Logger:
    """
    Konfiguruje logger dla biblioteki z logowaniem do konsoli i pliku.
    
    Args:
        name: Nazwa loggera.
        level: Poziom logowania (DEBUG, INFO, WARNING, ERROR).
        verbose: Czy używać szczegółowego formatowania.
        
    Returns:
        Skonfigurowany logger.
    """
    logger = logging.getLogger(name)
    
    # Usuń istniejące handlery
    logger.handlers = []
    
    # Ustaw poziom
    logger.setLevel(getattr(logging, level.upper()))
    
    # Handler do konsoli
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(getattr(logging, level.upper()))
    
    # Format dla konsoli (kolorowy jeśli dostępny)
    if COLORLOG_AVAILABLE:
        console_formatter = colorlog.ColoredFormatter(
            '%(log_color)s%(levelname)-8s%(reset)s %(blue)s%(message)s',
            datefmt=None,
            reset=True,
            log_colors={
                'DEBUG': 'cyan',
                'INFO': 'green',
                'WARNING': 'yellow',
                'ERROR': 'red',
                'CRITICAL': 'red,bg_white',
            }
        )
    else:
        if verbose:
            console_formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )
        else:
            console_formatter = logging.Formatter('%(levelname)-8s %(message)s')
    
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)
    
    # Handler do pliku z rotacją
    try:
        log_file = Path('dane_bez_twarzy.log')
        file_handler = RotatingFileHandler(
            log_file,
            maxBytes=10 * 1024 * 1024,  # 10 MB
            backupCount=5,  # Maksymalnie 5 plików archiwów
            encoding='utf-8'
        )
        file_handler.setLevel(logging.DEBUG)  # Zawsze loguj wszystko do pliku
        
        # Format dla pliku (zawsze szczegółowy)
        file_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)
        
    except Exception as e:
        # Jeśli nie można utworzyć pliku logu, kontynuuj bez niego
        logger.warning(f"Nie można utworzyć pliku logu: {e}")
    
    return logger
