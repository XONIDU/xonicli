@echo off
title XONICLI 2026 - Sistema Meteorologico en Terminal
color 0A

:: ============================================================
:: IR AL DIRECTORIO DONDE ESTA EL SCRIPT .BAT
:: ============================================================
cd /d "%~dp0"

:: ============================================================
:: VERIFICAR QUE start.py EXISTE
:: ============================================================
if not exist "%~dp0start.py" (
    echo [ERROR] No se encuentra start.py en esta carpeta
    echo.
    echo Ruta actual: %~dp0
    echo.
    echo Asegurate de que start.py esta en la misma carpeta que este .bat
    echo.
    pause
    exit /B
)

:: ============================================================
:: SOLICITAR PERMISOS DE ADMINISTRADOR (OPCIONAL, PERO RECOMENDADO)
:: ============================================================
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo Solicitando permisos de administrador...
    echo.
    echo Set UAC = CreateObject^("Shell.Application"^) > "%temp%\getadmin.vbs"
    echo UAC.ShellExecute "%~s0", "", "", "runas", 1 >> "%temp%\getadmin.vbs"
    "%temp%\getadmin.vbs"
    del "%temp%\getadmin.vbs"
    exit /B
)

:: ============================================================
:: EJECUTAR start.py
:: ============================================================
cls
echo ============================================================
echo           XONICLI 2026 - Sistema Meteorologico
echo ============================================================
echo.
echo [INFO] Directorio de trabajo: %~dp0
echo.
echo Iniciando XONICLI...
echo.
echo [INFO] Cliente meteorologico con animacion de la Tierra
echo [INFO] Fuente de datos: wttr.in
echo [INFO] Ubicaciones: %USERPROFILE%\.xonichat\ubicaciones.txt
echo [INFO] Cache de datos: %USERPROFILE%\.xonichat\weather_cache.json
echo.
echo [CARACTERISTICAS]
echo   - Tierra ASCII girando en tiempo real
echo   - Secuencia: hoy -> manana -> pasado manana
echo   - Dos modos: recurrente (bucle) o unica consulta
echo.
echo [COMANDOS]
echo   Presiona Ctrl+C para salir en cualquier momento
echo.
echo ============================================================
echo.

python start.py

if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Ocurrio un error al ejecutar XONICLI
    echo.
    echo Verifica que todos los archivos necesarios esten presentes
    echo y que Python este instalado correctamente.
    echo.
)

pause