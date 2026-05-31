@echo off
setlocal

REM === Definir archivo de log ===
set LOGFILE=C:\PRACTICAS POLITECNICO\Equipo_PP2-HRRG-2-2026\actualizar_llm.log
echo ===== Inicio de actualización: %date% %time% ===== >> %LOGFILE%

REM Intentar detectar PowerShell
where powershell >nul 2>&1
if %errorlevel%==0 (
    REM === Bloque PowerShell ===
    echo Ejecutando en PowerShell... >> %LOGFILE%
    powershell -NoProfile -ExecutionPolicy Bypass ^
        "Set-Location 'C:\PRACTICAS POLITECNICO\Equipo_PP2-HRRG-2-2026'; ^
         Add-Content -Path '%LOGFILE%' -Value '--- git pull ---'; ^
         git pull origin prueba-markdown-dario | Tee-Object -FilePath '%LOGFILE%' -Append; ^
         Add-Content -Path '%LOGFILE%' -Value '--- git status ---'; ^
         git status --short | Tee-Object -FilePath '%LOGFILE%' -Append; ^
         Write-Host '⚠️ Si Flask está corriendo, cerralo con CTRL+C antes de seguir.'; ^
         Pause; ^
         Add-Content -Path '%LOGFILE%' -Value '--- Borrando data/chroma ---'; ^
         Remove-Item -Recurse -Force .\data\chroma; ^
         Add-Content -Path '%LOGFILE%' -Value '--- Re-ingestando documentos ---'; ^
         python scripts\ingest_documents.py --force | Tee-Object -FilePath '%LOGFILE%' -Append; ^
         Add-Content -Path '%LOGFILE%' -Value '--- Levantando Flask ---'; ^
         python run.py | Tee-Object -FilePath '%LOGFILE%' -Append"
) else (
    REM === Bloque CMD ===
    echo Ejecutando en CMD... >> %LOGFILE%
    cd /d C:\PRACTICAS POLITECNICO\Equipo_PP2-HRRG-2-2026
    echo --- git pull --- >> %LOGFILE%
    git pull origin prueba-markdown-dario >> %LOGFILE% 2>&1
    echo --- git status --- >> %LOGFILE%
    git status --short >> %LOGFILE% 2>&1
    echo ⚠️ Si Flask está corriendo, cerralo con CTRL+C antes de seguir.
    pause
    echo --- Borrando data/chroma --- >> %LOGFILE%
    rmdir /s /q data\chroma
    echo --- Re-ingestando documentos --- >> %LOGFILE%
    python scripts\ingest_documents.py --force >> %LOGFILE% 2>&1
    echo --- Levantando Flask --- >> %LOGFILE%
    python run.py >> %LOGFILE% 2>&1
)

echo ===== Fin de actualización: %date% %time% ===== >> %LOGFILE%
endlocal
