@echo off
echo ================================================
echo    Sistema de Cafeteria - PROCAFECOL SA
echo    Instalador de Dependencias
echo ================================================
echo.

echo Verificando Python...
python --version
if %errorlevel% neq 0 (
    echo ERROR: Python no esta instalado o no esta en el PATH
    echo Por favor instale Python 3.7 o superior desde python.org
    pause
    exit /b 1
)

echo.
echo Instalando dependencias...
echo.

echo Instalando reportlab...
pip install reportlab
if %errorlevel% neq 0 (
    echo ERROR: No se pudo instalar reportlab
    pause
    exit /b 1
)

echo.
echo ================================================
echo    Instalacion completada exitosamente!
echo ================================================
echo.
echo Para ejecutar el sistema, use:
echo    python main.py
echo.
echo Presione cualquier tecla para continuar...
pause > nul