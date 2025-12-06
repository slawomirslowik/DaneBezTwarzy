# Budowanie standalone aplikacji Windows za pomocą Nuitka
#
# Użycie:
#   .\build_nuitka.ps1          - buduje wersję LITE (bez NLP)
#   .\build_nuitka.ps1 -full    - buduje wersję FULL (z NLP)

param(
    [switch]$full = $false
)

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Dane Bez Twarzy - Nuitka Builder" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Sprawdź czy Nuitka jest zainstalowane
try {
    python -c "import nuitka" 2>$null
} catch {
    Write-Host "[BŁĄD] Nuitka nie jest zainstalowane!" -ForegroundColor Red
    Write-Host ""
    Write-Host "Instaluję Nuitka..." -ForegroundColor Yellow
    pip install nuitka
    if ($LASTEXITCODE -ne 0) {
        Write-Host "[BŁĄD] Instalacja Nuitka nie powiodła się!" -ForegroundColor Red
        exit 1
    }
}

# Tworzenie katalogu dist
if (-not (Test-Path "dist")) {
    New-Item -ItemType Directory -Path "dist" | Out-Null
}

if ($full) {
    Write-Host "[INFO] Budowanie wersji FULL z NLP..." -ForegroundColor Yellow
    Write-Host "[UWAGA] To może potrwać 10-30 minut i zajmie ~600 MB" -ForegroundColor Yellow
    Write-Host ""
    
    python -m nuitka `
        --standalone `
        --onefile `
        --windows-console-mode=attach `
        --output-dir=dist `
        --output-filename=dane-bez-twarzy-full.exe `
        --enable-plugin=numpy `
        --include-package=spacy `
        --include-package=pl_core_news_lg `
        --include-package=dane_bez_twarzy `
        --include-data-dir=src/dane_bez_twarzy=dane_bez_twarzy `
        --company-name="Dane Bez Twarzy" `
        --product-name="Dane Bez Twarzy" `
        --file-version=1.0.0.0 `
        --product-version=1.0.0.0 `
        --file-description="Anonimizacja danych osobowych" `
        src/dane_bez_twarzy/cli.py
        
    if ($LASTEXITCODE -ne 0) {
        Write-Host "[BŁĄD] Budowanie nie powiodło się!" -ForegroundColor Red
        exit 1
    }
    
    Write-Host ""
    Write-Host "[SUKCES] Plik EXE: dist\dane-bez-twarzy-full.exe" -ForegroundColor Green
    Write-Host ""
    Write-Host "Testuj aplikację:" -ForegroundColor Cyan
    Write-Host "  .\dist\dane-bez-twarzy-full.exe anonymize input.txt -o output.txt --use-nlp" -ForegroundColor White
    
} else {
    Write-Host "[INFO] Budowanie wersji LITE bez NLP..." -ForegroundColor Yellow
    Write-Host "[INFO] Szybkie budowanie, mały rozmiar (~50 MB)" -ForegroundColor Yellow
    Write-Host ""
    
    python -m nuitka `
        --standalone `
        --onefile `
        --windows-console-mode=attach `
        --output-dir=dist `
        --output-filename=dane-bez-twarzy.exe `
        --nofollow-import-to=spacy `
        --nofollow-import-to=pl_core_news_lg `
        --include-package=dane_bez_twarzy `
        --include-data-dir=src/dane_bez_twarzy=dane_bez_twarzy `
        --company-name="Dane Bez Twarzy" `
        --product-name="Dane Bez Twarzy" `
        --file-version=1.0.0.0 `
        --product-version=1.0.0.0 `
        --file-description="Anonimizacja danych osobowych (Lite)" `
        src/dane_bez_twarzy/cli.py
        
    if ($LASTEXITCODE -ne 0) {
        Write-Host "[BŁĄD] Budowanie nie powiodło się!" -ForegroundColor Red
        exit 1
    }
    
    Write-Host ""
    Write-Host "[SUKCES] Plik EXE: dist\dane-bez-twarzy.exe" -ForegroundColor Green
    Write-Host "[INFO] Wersja LITE działa bez --use-nlp (Regex + LLM)" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Testuj aplikację:" -ForegroundColor Cyan
    Write-Host "  .\dist\dane-bez-twarzy.exe anonymize input.txt -o output.txt" -ForegroundColor White
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Budowanie zakończone!" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
