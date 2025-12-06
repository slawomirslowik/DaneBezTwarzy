"""
Logger setup for the library.
"""

import logging
import sys
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
    Konfiguruje logger dla biblioteki.
    
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
    
    # Format
    if COLORLOG_AVAILABLE:
        formatter = colorlog.ColoredFormatter(
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
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )
        else:
            formatter = logging.Formatter('%(levelname)s - %(message)s')
    
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    return logger
