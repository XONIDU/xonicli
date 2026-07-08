# 🌍 XONICLI

**Cliente meteorológico por terminal con animación ASCII de la Tierra**  
Optimizado para equipos de bajos recursos (ASUS Eee PC, Raspberry Pi, etc.)  
Desarrollado por Darian Alberto Camacho Salas – XONIDU

---

## 📋 Características

- ✅ Interfaz 100% terminal – rápida y ligera
- ✅ Tierra animada girando en tiempo real junto a los datos
- ✅ Múltiples ubicaciones (país + código postal)
- ✅ Datos en caché: solo una descarga por internet (modo sin conexión después)
- ✅ Secuencia automática: hoy → mañana → pasado mañana (cada 10 segundos)
- ✅ Dos modos: recurrente (bucle infinito) o consulta única (también con bucle)
- ✅ Gestor interactivo de ubicaciones – sin editar archivos manualmente
- ✅ Sin `sudo` – los archivos se guardan en `~/.xonichat/`
- ✅ Colores personalizables (0‑9) en toda la interfaz
- ✅ Compatible con Windows, Linux y macOS

---

## 📦 Instalación

### Para Linux/macOS

#### Opción 1 – Clonado manual

```bash
git clone https://github.com/XONIDU/xonicli.git
cd xonicli
pip install -r requirements.txt   # o solo pip install requests
python start.py
```

#### Opción 2 – Comando `xoninstall` (recomendado para futuras herramientas XONI)

Agrega la siguiente función a tu `~/.bashrc` con un solo comando:

```bash
echo 'xoninstall() { if [ -z "$1" ]; then echo "Uso: xoninstall <repo>"; echo "Ej: xoninstall xoniran"; else git clone "https://github.com/XONIDU/$1.git"; fi; }' >> ~/.bashrc && source ~/.bashrc && echo "✅ Listo. Usa: xoninstall xonicli"
```

Luego simplemente escribe:

```bash
xoninstall xonicli
cd xonicli
pip install -r requirements.txt
python start.py
```

> **Nota:** Esta función te servirá para instalar cualquier otra herramienta futura de XONIDU (por ejemplo `xoninstall xoniran`).

### Para Windows

#### Opción 1 – Clonado manual (PowerShell o CMD)

```cmd
git clone https://github.com/XONIDU/xonicli.git
cd xonicli
pip install -r requirements.txt
python start.py
```

#### Opción 2 – Usar `xonicli.bat` (con permisos de administrador)

Descarga o crea el archivo `xonicli.bat` en el mismo directorio con el siguiente contenido:

```batch
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
```

Haz doble clic en `xonicli.bat` para ejecutar XONICLI con permisos de administrador en Windows.

---

## 🔧 Configuración

La primera vez que ejecutes `start.py` se abrirá un gestor interactivo donde podrás:

- Elegir el color del texto (0‑9)
- Agregar una o varias ubicaciones (código postal + país)
- Seleccionar el modo de ejecución

### Archivo de ubicaciones (manual)

Si prefieres editar directamente el archivo, se encuentra en:

```
~/.xonichat/ubicaciones.txt   (Linux/macOS)
%USERPROFILE%\.xonichat\ubicaciones.txt   (Windows)
```

Formato (una ubicación por línea, **código postal** y **país** separados por espacio):

```
28001 ES
55660 MX
75001 FR
```

### Caché de datos meteorológicos

Los datos se guardan en `~/.xonichat/weather_cache.json`.  
Solo se descargan una vez (la primera ejecución). En ejecuciones posteriores se usan los datos guardados, ahorrando ancho de banda y permitiendo funcionar sin internet.

---

## 🚀 Uso

### Linux/macOS:
```bash
python start.py
```

### Windows:
- Opción 1: `python start.py` (CMD o PowerShell)
- Opción 2: Doble clic en `xonicli.bat`

Dentro del programa:

- El programa mostrará la Tierra girando junto a la información climática.
- Cada 10 segundos avanzará automáticamente al siguiente día (hoy → mañana → pasado mañana) y luego a la siguiente ubicación.
- En **modo recurrente** el ciclo se repite infinitamente.
- En **modo consulta única** también se repite infinitamente (ambos modos son ahora bucle infinito).
- Presiona `Ctrl+C` en cualquier momento para salir.

### Ejemplo de pantalla

```
============================================================
   XONICLI - SISTEMA METEOROLOGICO CON TIERRA ANIMADA
============================================================
   Fuente: wttr.in | Sin emojis | Cache local
   La Tierra gira en tiempo real junto a los datos
============================================================

 (Aquí aparece la Tierra ASCII girando a la izquierda)
 (A la derecha o debajo se ven los datos climáticos)
```

---

## 📁 Estructura del paquete

| Archivo | Ubicación |
|---------|-----------|
| `xonicli.py` (programa principal) | Directorio del proyecto |
| `start.py` (lanzador) | Directorio del proyecto |
| `xonicli.bat` (lanzador Windows) | Directorio del proyecto |
| `ubicaciones.txt` | `~/.xonichat/` (Linux) o `%USERPROFILE%\.xonichat\` (Windows) |
| `weather_cache.json` | `~/.xonichat/` (Linux) o `%USERPROFILE%\.xonichat\` (Windows) |

---

## 🧪 Pruebas

Ejecuta directamente el script principal:

```bash
python xonicli.py
```

Si todo funciona correctamente, verás la animación de la Tierra y los datos del clima.

---

## 🐛 Problemas comunes y soluciones

| Problema | Solución |
|----------|----------|
| `No module 'requests'` | `pip install requests` (o `pip3 install requests`) |
| Error `expected a nonnegative input` | Ya corregido en la última versión. Asegúrate de tener la versión más reciente. |
| La animación parpadea | Aumenta el tamaño de la terminal (mínimo 80x24). |
| No se ven datos | En la primera ejecución se necesita internet. Luego ya funciona sin conexión. |
| `Permission denied` al ejecutar (Linux) | Usa `python start.py` en lugar de `./` o da permisos con `chmod +x start.py` |
| Error de permisos en Windows | Usa `xonicli.bat` que ejecuta con permisos de administrador |

---

## 📄 Licencia

**© 2026 Darian Alberto Camacho Salas (XONIDU)**  
Todos los derechos reservados. No se permite la copia, distribución o modificación sin autorización explícita.

---

## ✉️ Contacto

- **Creador**: Darian Alberto Camacho Salas  
- **Email**: xonidu@gmail.com  
- **GitHub**: [@XONIDU](https://github.com/XONIDU)

---

*Hecho con 🌍 y código para los amantes de la terminal.*
