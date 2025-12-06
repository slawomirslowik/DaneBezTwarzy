"""
Generator raportów HTML z interaktywnymi wykresami.
"""

from pathlib import Path
from typing import Dict, Any
import json


def generate_html_report(report: Dict[str, Any], output_path: Path) -> None:
    """
    Generuje wizualny raport HTML z wykresami Plotly.
    
    Args:
        report: Słownik z raportem z anonimizacji.
        output_path: Ścieżka do pliku HTML.
    """
    
    # Przygotowanie danych dla wykresów
    entity_types = list(report['entities_by_type'].keys())
    entity_counts = list(report['entities_by_type'].values())
    
    # Kolory dla wykresów
    colors = ['#3498db', '#e74c3c', '#2ecc71', '#f39c12', '#9b59b6', '#1abc9c', 
              '#34495e', '#16a085', '#c0392b', '#d35400', '#8e44ad', '#27ae60']
    
    html = f"""<!DOCTYPE html>
<html lang="pl">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Raport Anonimizacji - {report['file_stats']['filename'] or 'Dokument'}</title>
    <script src="https://cdn.plot.ly/plotly-2.27.0.min.js"></script>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
            min-height: 100vh;
        }}
        
        .container {{
            max-width: 1400px;
            margin: 0 auto;
            background: white;
            padding: 40px;
            border-radius: 12px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.2);
        }}
        
        header {{
            border-bottom: 4px solid #667eea;
            padding-bottom: 20px;
            margin-bottom: 30px;
        }}
        
        h1 {{
            color: #2c3e50;
            font-size: 32px;
            margin-bottom: 10px;
        }}
        
        .subtitle {{
            color: #7f8c8d;
            font-size: 16px;
        }}
        
        .config {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 25px;
            border-radius: 8px;
            margin: 20px 0;
        }}
        
        .config h3 {{
            margin-bottom: 15px;
            font-size: 20px;
        }}
        
        .config-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
        }}
        
        .config-item {{
            background: rgba(255,255,255,0.1);
            padding: 12px;
            border-radius: 6px;
        }}
        
        .config-label {{
            font-size: 12px;
            opacity: 0.9;
            margin-bottom: 5px;
        }}
        
        .config-value {{
            font-size: 18px;
            font-weight: bold;
        }}
        
        .stats {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
            gap: 20px;
            margin: 30px 0;
        }}
        
        .stat-card {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 25px;
            border-radius: 10px;
            text-align: center;
            box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
            transition: transform 0.3s ease;
        }}
        
        .stat-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
        }}
        
        .stat-value {{
            font-size: 48px;
            font-weight: bold;
            margin-bottom: 10px;
        }}
        
        .stat-label {{
            font-size: 14px;
            opacity: 0.95;
            text-transform: uppercase;
            letter-spacing: 1px;
        }}
        
        .chart-section {{
            margin: 40px 0;
        }}
        
        .chart-title {{
            font-size: 22px;
            color: #2c3e50;
            margin-bottom: 20px;
            padding-left: 10px;
            border-left: 4px solid #667eea;
        }}
        
        .chart {{
            background: #f8f9fa;
            padding: 20px;
            border-radius: 8px;
            margin-bottom: 30px;
        }}
        
        .entity-table {{
            margin-top: 40px;
        }}
        
        table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        
        th {{
            background: #667eea;
            color: white;
            padding: 15px;
            text-align: left;
            font-weight: 600;
        }}
        
        td {{
            padding: 12px 15px;
            border-bottom: 1px solid #ecf0f1;
        }}
        
        tr:hover {{
            background: #f8f9fa;
        }}
        
        .badge {{
            display: inline-block;
            padding: 5px 12px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: bold;
            background: #3498db;
            color: white;
        }}
        
        .confidence-bar {{
            height: 6px;
            background: #ecf0f1;
            border-radius: 3px;
            overflow: hidden;
        }}
        
        .confidence-fill {{
            height: 100%;
            background: #2ecc71;
            transition: width 0.3s ease;
        }}
        
        footer {{
            margin-top: 40px;
            padding-top: 20px;
            border-top: 1px solid #ecf0f1;
            text-align: center;
            color: #7f8c8d;
            font-size: 14px;
        }}
        
        @media print {{
            body {{
                background: white;
                padding: 0;
            }}
            .container {{
                box-shadow: none;
            }}
            .stat-card:hover {{
                transform: none;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>📊 Raport Anonimizacji</h1>
            <p class="subtitle">Automatyczna analiza i anonimizacja danych osobowych</p>
        </header>
        
        <div class="config">
            <h3>⚙️ Konfiguracja procesu</h3>
            <div class="config-grid">
                <div class="config-item">
                    <div class="config-label">Plik źródłowy</div>
                    <div class="config-value">{report['file_stats']['filename'] or 'N/A'}</div>
                </div>
                <div class="config-item">
                    <div class="config-label">Metoda</div>
                    <div class="config-value">{report['config']['method'].upper()}</div>
                </div>
                <div class="config-item">
                    <div class="config-label">Język</div>
                    <div class="config-value">{report['config']['language'].upper()}</div>
                </div>
                <div class="config-item">
                    <div class="config-label">NLP</div>
                    <div class="config-value">{'✅ Włączony' if report['config']['use_nlp'] else '❌ Wyłączony'}</div>
                </div>
                <div class="config-item">
                    <div class="config-label">LLM (PLLUM)</div>
                    <div class="config-value">{'✅ Włączony' if report['config']['use_llm'] else '❌ Wyłączony'}</div>
                </div>
                <div class="config-item">
                    <div class="config-label">Czas wykonania</div>
                    <div class="config-value">{report.get('execution_time_seconds', 0):.2f}s</div>
                </div>
            </div>
        </div>
        
        <div class="stats">
            <div class="stat-card">
                <div class="stat-value">{report['file_stats']['line_count']:,}</div>
                <div class="stat-label">Linii</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{report['file_stats']['character_count']:,}</div>
                <div class="stat-label">Znaków</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{report['total_entities']:,}</div>
                <div class="stat-label">Wykrytych encji</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{len(report['entities_by_type'])}</div>
                <div class="stat-label">Typów encji</div>
            </div>
        </div>
        
        <div class="chart-section">
            <h2 class="chart-title">Rozkład typów encji</h2>
            <div class="chart" id="pieChart"></div>
        </div>
        
        <div class="chart-section">
            <h2 class="chart-title">Liczba encji według typu</h2>
            <div class="chart" id="barChart"></div>
        </div>
        
        <div class="entity-table">
            <h2 class="chart-title">Wykryte encje (pierwszych 50)</h2>
            <table>
                <thead>
                    <tr>
                        <th>#</th>
                        <th>Typ</th>
                        <th>Tekst</th>
                        <th>Pozycja</th>
                        <th>Pewność</th>
                        <th>Detektor</th>
                    </tr>
                </thead>
                <tbody>
"""
    
    # Dodaj wiersze tabeli (max 50 encji)
    for i, entity in enumerate(report['entities'][:50], 1):
        confidence = entity.get('confidence', 1.0)
        confidence_percent = int(confidence * 100)
        
        html += f"""                    <tr>
                        <td>{i}</td>
                        <td><span class="badge">{entity['type']}</span></td>
                        <td>{entity.get('text', 'N/A')[:50]}</td>
                        <td>{entity.get('start', 'N/A')}-{entity.get('end', 'N/A')}</td>
                        <td>
                            <div class="confidence-bar">
                                <div class="confidence-fill" style="width: {confidence_percent}%"></div>
                            </div>
                            {confidence_percent}%
                        </td>
                        <td>{entity.get('metadata', {}).get('detector', 'N/A')}</td>
                    </tr>
"""
    
    html += f"""                </tbody>
            </table>
            {f'<p style="margin-top: 15px; color: #7f8c8d;">Wyświetlono 50 z {len(report["entities"])} encji</p>' if len(report['entities']) > 50 else ''}
        </div>
        
        <footer>
            <p>Wygenerowano przez <strong>Dane Bez Twarzy</strong> - Biblioteka anonimizacji danych osobowych</p>
            <p style="margin-top: 5px;">Data: {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        </footer>
    </div>
    
    <script>
        // Wykres kołowy
        var pieData = [{{
            values: {entity_counts},
            labels: {entity_types},
            type: 'pie',
            hole: 0.4,
            marker: {{
                colors: {colors[:len(entity_types)]},
                line: {{ color: 'white', width: 2 }}
            }},
            textinfo: 'label+percent',
            textposition: 'outside',
            hovertemplate: '<b>%{{label}}</b><br>Liczba: %{{value}}<br>Udział: %{{percent}}<extra></extra>'
        }}];
        
        var pieLayout = {{
            height: 500,
            showlegend: true,
            legend: {{
                orientation: 'h',
                y: -0.2
            }},
            margin: {{ t: 20, b: 100 }}
        }};
        
        var pieConfig = {{
            responsive: true,
            displayModeBar: true,
            displaylogo: false
        }};
        
        Plotly.newPlot('pieChart', pieData, pieLayout, pieConfig);
        
        // Wykres słupkowy
        var barData = [{{
            x: {entity_types},
            y: {entity_counts},
            type: 'bar',
            marker: {{
                color: {colors[:len(entity_types)]},
                line: {{ color: 'white', width: 1.5 }}
            }},
            hovertemplate: '<b>%{{x}}</b><br>Liczba: %{{y}}<extra></extra>'
        }}];
        
        var barLayout = {{
            height: 500,
            xaxis: {{ 
                title: 'Typ encji',
                tickangle: -45
            }},
            yaxis: {{ 
                title: 'Liczba wykryć',
                gridcolor: '#ecf0f1'
            }},
            margin: {{ b: 120 }}
        }};
        
        var barConfig = {{
            responsive: true,
            displayModeBar: true,
            displaylogo: false
        }};
        
        Plotly.newPlot('barChart', barData, barLayout, barConfig);
    </script>
</body>
</html>
"""
    
    output_path = Path(output_path)
    output_path.write_text(html, encoding='utf-8')
