@echo off
echo ================================================
echo    Sistema de Cafeteria - PROCAFECOL SA
echo ================================================
echo.
echo Iniciando sistema...
echo.

python main.py

if %errorlevel% neq 0 (
    echo.
    echo ERROR: No se pudo ejecutar el sistema
    echo Verifique que Python este instalado y las dependencias esten correctas
    echo.
    echo Para instalar dependencias ejecute: instalar.bat
    echo.
    pause
)