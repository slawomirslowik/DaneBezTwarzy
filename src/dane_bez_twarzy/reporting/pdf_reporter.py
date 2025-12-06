"""
Generator raportów PDF z wykresami matplotlib.
"""

from pathlib import Path
from typing import Dict, Any
import matplotlib
matplotlib.use('Agg')  # Backend bez GUI
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import datetime


def generate_pdf_report(report: Dict[str, Any], output_path: Path) -> None:
    """
    Generuje raport PDF z wykresami matplotlib.
    
    Args:
        report: Słownik z raportem z anonimizacji.
        output_path: Ścieżka do pliku PDF.
    """
    
    with PdfPages(output_path) as pdf:
        # Strona 1: Statystyki główne
        fig = plt.figure(figsize=(11, 8))
        fig.suptitle(f"Raport Anonimizacji\n{report['file_stats']['filename'] or 'Dokument'}", 
                     fontsize=16, fontweight='bold', y=0.98)
        
        # Siatka 2x2
        gs = fig.add_gridspec(2, 2, hspace=0.3, wspace=0.3)
        
        # 1. Wykres kołowy - rozkład typów encji
        ax1 = fig.add_subplot(gs[0, 0])
        entity_types = list(report['entities_by_type'].keys())
        entity_counts = list(report['entities_by_type'].values())
        
        colors = plt.cm.Set3(range(len(entity_types)))
        wedges, texts, autotexts = ax1.pie(
            entity_counts, 
            labels=entity_types,
            autopct='%1.1f%%',
            colors=colors,
            startangle=90,
            textprops={'fontsize': 9}
        )
        ax1.set_title('Rozkład typów encji', fontweight='bold', pad=15)
        
        # 2. Wykres słupkowy - liczba encji
        ax2 = fig.add_subplot(gs[0, 1])
        bars = ax2.bar(range(len(entity_types)), entity_counts, color=colors)
        ax2.set_xticks(range(len(entity_types)))
        ax2.set_xticklabels(entity_types, rotation=45, ha='right', fontsize=8)
        ax2.set_ylabel('Liczba wykryć', fontweight='bold')
        ax2.set_title('Liczba encji według typu', fontweight='bold', pad=15)
        ax2.grid(axis='y', alpha=0.3)
        
        # Dodaj wartości na słupkach
        for bar in bars:
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., height,
                    f'{int(height)}',
                    ha='center', va='bottom', fontsize=8)
        
        # 3. Tabela statystyk pliku
        ax3 = fig.add_subplot(gs[1, 0])
        ax3.axis('off')
        
        stats_data = [
            ['Parametr', 'Wartość'],
            ['Linii w pliku', f"{report['file_stats']['line_count']:,}"],
            ['Znaków w pliku', f"{report['file_stats']['character_count']:,}"],
            ['Wykrytych encji', f"{report['total_entities']:,}"],
            ['Typów encji', str(len(report['entities_by_type']))],
            ['Czas wykonania', f"{report.get('execution_time_seconds', 0):.3f}s"]
        ]
        
        table = ax3.table(
            cellText=stats_data,
            cellLoc='left',
            loc='center',
            colWidths=[0.5, 0.5]
        )
        table.auto_set_font_size(False)
        table.set_fontsize(9)
        table.scale(1, 2)
        
        # Styl nagłówka
        for i in range(2):
            table[(0, i)].set_facecolor('#667eea')
            table[(0, i)].set_text_props(weight='bold', color='white')
        
        # Styl wierszy
        for i in range(1, len(stats_data)):
            for j in range(2):
                if i % 2 == 0:
                    table[(i, j)].set_facecolor('#f0f0f0')
        
        ax3.set_title('Statystyki pliku', fontweight='bold', pad=20, loc='left')
        
        # 4. Tabela konfiguracji
        ax4 = fig.add_subplot(gs[1, 1])
        ax4.axis('off')
        
        config_data = [
            ['Parametr', 'Wartość'],
            ['Metoda', report['config']['method'].upper()],
            ['Język', report['config']['language'].upper()],
            ['Min. pewność', f"{report['config']['min_confidence']:.2f}"],
            ['NLP', '✓ Włączony' if report['config']['use_nlp'] else '✗ Wyłączony'],
            ['LLM', '✓ Włączony' if report['config']['use_llm'] else '✗ Wyłączony']
        ]
        
        config_table = ax4.table(
            cellText=config_data,
            cellLoc='left',
            loc='center',
            colWidths=[0.5, 0.5]
        )
        config_table.auto_set_font_size(False)
        config_table.set_fontsize(9)
        config_table.scale(1, 2)
        
        # Styl nagłówka
        for i in range(2):
            config_table[(0, i)].set_facecolor('#764ba2')
            config_table[(0, i)].set_text_props(weight='bold', color='white')
        
        # Styl wierszy
        for i in range(1, len(config_data)):
            for j in range(2):
                if i % 2 == 0:
                    config_table[(i, j)].set_facecolor('#f0f0f0')
        
        ax4.set_title('Konfiguracja', fontweight='bold', pad=20, loc='left')
        
        # Stopka
        fig.text(0.5, 0.02, 
                f'Wygenerowano: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")} | '
                f'Dane Bez Twarzy - Biblioteka anonimizacji',
                ha='center', fontsize=8, style='italic', color='gray')
        
        pdf.savefig(fig, bbox_inches='tight')
        plt.close()
        
        # Strona 2: Szczegółowa lista encji (jeśli jest ich więcej niż 0)
        if report['entities']:
            entities_per_page = 35
            total_pages = (len(report['entities']) + entities_per_page - 1) // entities_per_page
            
            for page in range(total_pages):
                fig, ax = plt.subplots(figsize=(11, 8))
                ax.axis('off')
                
                start_idx = page * entities_per_page
                end_idx = min((page + 1) * entities_per_page, len(report['entities']))
                page_entities = report['entities'][start_idx:end_idx]
                
                # Przygotuj dane dla tabeli
                table_data = [['#', 'Typ', 'Tekst', 'Pozycja', 'Pewność', 'Detektor']]
                
                for i, entity in enumerate(page_entities, start=start_idx + 1):
                    text = entity.get('text', 'N/A')
                    if len(text) > 30:
                        text = text[:27] + '...'
                    
                    table_data.append([
                        str(i),
                        entity['type'],
                        text,
                        f"{entity.get('start', 'N/A')}-{entity.get('end', 'N/A')}",
                        f"{entity.get('confidence', 1.0):.2f}",
                        entity.get('metadata', {}).get('detector', 'N/A')
                    ])
                
                # Utwórz tabelę
                table = ax.table(
                    cellText=table_data,
                    cellLoc='left',
                    loc='center',
                    colWidths=[0.05, 0.15, 0.35, 0.15, 0.10, 0.20]
                )
                table.auto_set_font_size(False)
                table.set_fontsize(8)
                table.scale(1, 1.5)
                
                # Styl nagłówka
                for i in range(6):
                    table[(0, i)].set_facecolor('#667eea')
                    table[(0, i)].set_text_props(weight='bold', color='white')
                
                # Styl wierszy
                for i in range(1, len(table_data)):
                    for j in range(6):
                        if i % 2 == 0:
                            table[(i, j)].set_facecolor('#f8f8f8')
                
                fig.suptitle(
                    f'Wykryte encje (strona {page + 1}/{total_pages})\n'
                    f'Encje {start_idx + 1}-{end_idx} z {len(report["entities"])}',
                    fontsize=14, fontweight='bold', y=0.98
                )
                
                pdf.savefig(fig, bbox_inches='tight')
                plt.close()
