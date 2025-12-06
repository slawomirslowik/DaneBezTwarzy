"""
CLI (Command Line Interface) dla biblioteki.
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Optional

from dane_bez_twarzy import Anonymizer, AnonymizationConfig


def main() -> None:
    """Główna funkcja CLI."""
    parser = argparse.ArgumentParser(
        description='Dane Bez Twarzy - Anonimizacja danych osobowych',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Dostępne komendy')
    
    # Komenda: anonymize
    anonymize_parser = subparsers.add_parser('anonymize', help='Anonimizuj pojedynczy plik')
    anonymize_parser.add_argument('input', type=str, help='Ścieżka do pliku wejściowego')
    anonymize_parser.add_argument('-o', '--output', type=str, help='Ścieżka do pliku wyjściowego')
    anonymize_parser.add_argument('-c', '--config', type=str, help='Ścieżka do pliku konfiguracyjnego JSON')
    anonymize_parser.add_argument('-m', '--method', type=str, 
                                   choices=['mask', 'entity', 'pseudonymize', 'hash', 'redact', 'generalize', 'encrypt'],
                                   default='mask', help='Metoda anonimizacji')
    anonymize_parser.add_argument('--language', type=str, default='pl', help='Język dokumentu')
    anonymize_parser.add_argument('--use-nlp', action='store_true', help='Włącz NLP (wykrywanie imion/nazwisk)')
    anonymize_parser.add_argument('--no-nlp', action='store_true', help='Wyłącz NLP (domyślnie wyłączone)')
    anonymize_parser.add_argument('--use-llm', action='store_true', help='Włącz detektor LLM (PLLUM)')
    anonymize_parser.add_argument('--llm-api-key', type=str, help='Klucz API do LLM')
    anonymize_parser.add_argument('--llm-base-url', type=str, help='URL bazowy API LLM')
    anonymize_parser.add_argument('--llm-model', type=str, help='Nazwa modelu LLM')
    anonymize_parser.add_argument('-v', '--verbose', action='store_true', help='Tryb szczegółowy')
    
    # Komenda: anonymize-dir
    dir_parser = subparsers.add_parser('anonymize-dir', help='Anonimizuj katalog')
    dir_parser.add_argument('input_dir', type=str, help='Katalog wejściowy')
    dir_parser.add_argument('-o', '--output-dir', type=str, required=True, help='Katalog wyjściowy')
    dir_parser.add_argument('-r', '--recursive', action='store_true', help='Przetwarzaj rekurencyjnie')
    dir_parser.add_argument('-p', '--patterns', type=str, nargs='+', 
                           default=['*.txt', '*.docx', '*.xlsx', '*.pdf'],
                           help='Wzorce plików do przetworzenia')
    dir_parser.add_argument('-c', '--config', type=str, help='Ścieżka do pliku konfiguracyjnego JSON')
    dir_parser.add_argument('--use-nlp', action='store_true', help='Włącz NLP (wykrywanie imion/nazwisk)')
    dir_parser.add_argument('--no-nlp', action='store_true', help='Wyłącz NLP (domyślnie wyłączone)')
    dir_parser.add_argument('--use-llm', action='store_true', help='Włącz detektor LLM (PLLUM)')
    dir_parser.add_argument('--llm-api-key', type=str, help='Klucz API do LLM')
    dir_parser.add_argument('--llm-base-url', type=str, help='URL bazowy API LLM')
    dir_parser.add_argument('--llm-model', type=str, help='Nazwa modelu LLM')
    dir_parser.add_argument('-v', '--verbose', action='store_true', help='Tryb szczegółowy')
    
    # Komenda: detect
    detect_parser = subparsers.add_parser('detect', help='Wykryj encje bez anonimizacji')
    detect_parser.add_argument('input', type=str, help='Ścieżka do pliku')
    detect_parser.add_argument('-r', '--report', type=str, help='Ścieżka do zapisu raportu')
    detect_parser.add_argument('-c', '--config', type=str, help='Ścieżka do pliku konfiguracyjnego JSON')
    detect_parser.add_argument('--use-nlp', action='store_true', help='Włącz NLP (wykrywanie imion/nazwisk)')
    detect_parser.add_argument('--no-nlp', action='store_true', help='Wyłącz NLP')
    detect_parser.add_argument('--use-llm', action='store_true', help='Włącz detektor LLM (PLLUM)')
    detect_parser.add_argument('--llm-api-key', type=str, help='Klucz API do LLM')
    detect_parser.add_argument('--llm-base-url', type=str, help='URL bazowy API LLM')
    detect_parser.add_argument('--llm-model', type=str, help='Nazwa modelu LLM')
    detect_parser.add_argument('-v', '--verbose', action='store_true', help='Tryb szczegółowy')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    # Wykonaj komendę
    try:
        if args.command == 'anonymize':
            anonymize_file(args)
        elif args.command == 'anonymize-dir':
            anonymize_directory(args)
        elif args.command == 'detect':
            detect_entities(args)
    except Exception as e:
        print(f"Błąd: {e}", file=sys.stderr)
        sys.exit(1)


def load_config(config_path: Optional[str], args) -> AnonymizationConfig:
    """Ładuje konfigurację z pliku lub argumentów."""
    if config_path:
        with open(config_path, 'r', encoding='utf-8') as f:
            config_dict = json.load(f)
        config = AnonymizationConfig(**config_dict)
    else:
        config_kwargs = {}
        if hasattr(args, 'method'):
            config_kwargs['method'] = args.method
        if hasattr(args, 'language'):
            config_kwargs['language'] = args.language
        
        # Obsługa flag NLP (--use-nlp ma priorytet nad --no-nlp)
        if hasattr(args, 'use_nlp') and args.use_nlp:
            config_kwargs['use_nlp'] = True
        elif hasattr(args, 'no_nlp') and args.no_nlp:
            config_kwargs['use_nlp'] = False
        # Jeśli brak flag, użyje domyślnej wartości z config.py (False)
        
        if hasattr(args, 'verbose'):
            config_kwargs['verbose'] = args.verbose
            config_kwargs['log_level'] = 'DEBUG' if args.verbose else 'INFO'
        
        config = AnonymizationConfig(**config_kwargs)
    
    return config


def anonymize_file(args) -> None:
    """Anonimizuje pojedynczy plik."""
    config = load_config(args.config, args)
    
    # Parametry LLM
    llm_kwargs = {}
    if hasattr(args, 'use_llm') and args.use_llm:
        llm_kwargs['use_llm'] = True
        if hasattr(args, 'llm_api_key') and args.llm_api_key:
            llm_kwargs['llm_api_key'] = args.llm_api_key
        if hasattr(args, 'llm_base_url') and args.llm_base_url:
            llm_kwargs['llm_base_url'] = args.llm_base_url
        if hasattr(args, 'llm_model') and args.llm_model:
            llm_kwargs['llm_model_name'] = args.llm_model
    
    anonymizer = Anonymizer(config, **llm_kwargs)
    
    input_path = Path(args.input)
    output_path = Path(args.output) if args.output else None
    
    result_path = anonymizer.anonymize_file(input_path, output_path)
    print(f"✓ Plik zanonimizowany: {result_path}")


def anonymize_directory(args) -> None:
    """Anonimizuje katalog."""
    config = load_config(args.config, args)
    
    # Parametry LLM
    llm_kwargs = {}
    if hasattr(args, 'use_llm') and args.use_llm:
        llm_kwargs['use_llm'] = True
        if hasattr(args, 'llm_api_key') and args.llm_api_key:
            llm_kwargs['llm_api_key'] = args.llm_api_key
        if hasattr(args, 'llm_base_url') and args.llm_base_url:
            llm_kwargs['llm_base_url'] = args.llm_base_url
        if hasattr(args, 'llm_model') and args.llm_model:
            llm_kwargs['llm_model_name'] = args.llm_model
    
    anonymizer = Anonymizer(config, **llm_kwargs)
    
    input_dir = Path(args.input_dir)
    output_dir = Path(args.output_dir)
    
    results = anonymizer.anonymize_directory(
        input_dir=input_dir,
        output_dir=output_dir,
        recursive=args.recursive,
        file_patterns=args.patterns
    )
    
    print(f"✓ Przetworzono {len(results)} plików")
    print(f"✓ Wyniki zapisane w: {output_dir}")


def detect_entities(args) -> None:
    """Wykrywa encje w pliku."""
    config = load_config(args.config, args)
    
    # Parametry LLM
    llm_kwargs = {}
    if hasattr(args, 'use_llm') and args.use_llm:
        llm_kwargs['use_llm'] = True
        if hasattr(args, 'llm_api_key') and args.llm_api_key:
            llm_kwargs['llm_api_key'] = args.llm_api_key
        if hasattr(args, 'llm_base_url') and args.llm_base_url:
            llm_kwargs['llm_base_url'] = args.llm_base_url
        if hasattr(args, 'llm_model') and args.llm_model:
            llm_kwargs['llm_model_name'] = args.llm_model
    
    anonymizer = Anonymizer(config, **llm_kwargs)
    
    input_path = Path(args.input)
    
    # Wczytaj tekst
    with open(input_path, 'r', encoding='utf-8') as f:
        text = f.read()
    
    # Wygeneruj raport
    report_path = Path(args.report) if args.report else None
    report = anonymizer.generate_report(text, report_path)
    
    # Wyświetl statystyki
    print(f"✓ Znaleziono {report['total_entities']} encji")
    print("\nStatystyki według typu:")
    for entity_type, count in report['entities_by_type'].items():
        print(f"  - {entity_type}: {count}")
    
    if report_path:
        print(f"\n✓ Raport zapisany: {report_path}")


if __name__ == '__main__':
    main()
