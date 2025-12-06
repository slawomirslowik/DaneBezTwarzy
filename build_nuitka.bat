@echo off
REM Skrypt budowania standalone aplikacji Windows za pomocą Nuitka
REM 
REM Użycie:
REM   build_nuitka.bat          - buduje wersję LITE (bez NLP)
REM   build_nuitka.bat full     - buduje wersję FULL (z NLP)

echo ========================================
echo   Dane Bez Twarzy - Nuitka Builder
echo ========================================
echo.

REM Sprawdź czy Nuitka jest zainstalowane
python -c "import nuitka" 2>nul
if errorlevel 1 (
    echo [BŁĄD] Nuitka nie jest zainstalowane!
    echo.
    echo Instaluję Nuitka...
    pip install nuitka
    if errorlevel 1 (
        echo [BŁĄD] Instalacja Nuitka nie powiodła się!
        pause
        exit /b 1
    )
)

REM Tworzenie katalogu dist
if not exist "dist" mkdir dist

REM Sprawdź argument (lite lub full)
set BUILD_TYPE=%1
if "%BUILD_TYPE%"=="" set BUILD_TYPE=lite

if /I "%BUILD_TYPE%"=="full" (
    echo [INFO] Budowanie wersji FULL z NLP...
    echo [UWAGA] To może potrwać 10-30 minut i zajmie ~600 MB
    echo.
    
    python -m nuitka ^
        --standalone ^
        --onefile ^
        --windows-console-mode=attach ^
        --output-dir=dist ^
        --output-filename=dane-bez-twarzy-full.exe ^
        --enable-plugin=numpy ^
        --include-package=spacy ^
        --include-package=pl_core_news_lg ^
        --include-package=dane_bez_twarzy ^
        --include-data-dir=src/dane_bez_twarzy=dane_bez_twarzy ^
        --company-name="Dane Bez Twarzy" ^
        --product-name="Dane Bez Twarzy" ^
        --file-version=1.0.0.0 ^
        --product-version=1.0.0.0 ^
        --file-description="Anonimizacja danych osobowych" ^
        src/dane_bez_twarzy/cli.py
        
    if errorlevel 1 (
        echo [BŁĄD] Budowanie nie powiodło się!
        pause
        exit /b 1
    )
    
    echo.
    echo [SUKCES] Plik EXE: dist\dane-bez-twarzy-full.exe
    
) else (
    echo [INFO] Budowanie wersji LITE bez NLP...
    echo [INFO] Szybkie budowanie, mały rozmiar (~50 MB)
    echo.
    
    python -m nuitka ^
        --standalone ^
        --onefile ^
        --windows-console-mode=attach ^
        --output-dir=dist ^
        --output-filename=dane-bez-twarzy.exe ^
        --nofollow-import-to=spacy ^
        --nofollow-import-to=pl_core_news_lg ^
        --include-package=dane_bez_twarzy ^
        --include-data-dir=src/dane_bez_twarzy=dane_bez_twarzy ^
        --company-name="Dane Bez Twarzy" ^
        --product-name="Dane Bez Twarzy" ^
        --file-version=1.0.0.0 ^
        --product-version=1.0.0.0 ^
        --file-description="Anonimizacja danych osobowych (Lite)" ^
        src/dane_bez_twarzy/cli.py
        
    if errorlevel 1 (
        echo [BŁĄD] Budowanie nie powiodło się!
        pause
        exit /b 1
    )
    
    echo.
    echo [SUKCES] Plik EXE: dist\dane-bez-twarzy.exe
    echo [INFO] Wersja LITE działa bez --use-nlp (Regex + LLM)
)

echo.
echo ========================================
echo   Budowanie zakończone!
echo ========================================
echo.
echo Testuj aplikację:
if /I "%BUILD_TYPE%"=="full" (
    echo   dist\dane-bez-twarzy-full.exe anonymize input.txt -o output.txt --use-nlp
) else (
    echo   dist\dane-bez-twarzy.exe anonymize input.txt -o output.txt
)
echo.

pause
