@echo off
title XONICLI 2026 - Sistema Meteorologico
color 0A

:: ============================================================
:: SOLICITAR PERMISOS DE ADMINISTRADOR
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
:: EJECUTAR start.py CON PERMISOS DE ADMINISTRADOR
:: ============================================================
cls
echo ============================================================
echo           XONICLI 2026 - Sistema Meteorologico
echo              (Modo Administrador)
echo ============================================================
echo.
echo [OK] Permisos de administrador obtenidos
echo.
echo Iniciando XONICLI...
echo.
echo [INFO] Sistema meteorologico con animacion de la Tierra
echo [INFO] Presiona Ctrl+C para salir
echo.
echo ============================================================
echo.

python start_weather.py

if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Ocurrio un error al ejecutar start_weather.py
    echo.
    echo Verifica que start_weather.py este en el mismo directorio
    echo.
)

pause
