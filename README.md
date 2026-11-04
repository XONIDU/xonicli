```markdown
# MONITOR WEB

**Monitor multiuso de terminal y escritorio: clima con animacion ASCII o paneles web en cuadricula**  
Optimizado para equipos de bajos recursos (ASUS Eee PC, Raspberry Pi, etc.)  
Desarrollado por Darian Alberto Camacho Salas — XONIDU

---

## Descripcion general

MONITOR WEB es una aplicacion que reúne dos herramientas en un solo lanzador:

1. **CLI (terminal)**: monitor meteorologico con animacion ASCII de la Tierra, multiples ubicaciones y cache local.
2. **UI (escritorio)**: visor de multiples paginas web en una cuadricula, con refresco automatico por panel, maximizacion y configuracion persistente.

El lanzador `start.py` detecta el sistema, verifica Python y pip, instala las dependencias necesarias segun el modo elegido (PyQt6 para la UI, `requests` + `beautifulsoup4` para el CLI) y ejecuta el programa correspondiente.

---

## Caracteristicas

### Modo CLI — Clima en terminal

| Caracteristica | Descripcion |
|----------------|-------------|
| Interfaz 100% terminal | Sin dependencias de escritorio |
| Animacion ASCII de la Tierra | Representacion continua del planeta junto a los datos |
| Multiples ubicaciones | Varias ubicaciones (pais + codigo postal) |
| Cache local | Los datos se descargan una sola vez y se reutilizan sin conexion |
| Secuencia automatica | Recorre hoy, manana y pasado manana cada 10 segundos |
| Bucle infinito | Ambos modos (recurrente y unica vez) se ejecutan hasta `Ctrl+C` |
| Colores personalizables | Seleccion de color de texto (0-9) |

### Modo UI — Paneles web en escritorio

| Caracteristica | Descripcion |
|----------------|-------------|
| Cuadricula de paneles | Varias webs visibles a la vez |
| Refresco automatico | Configurable por panel (minutos) |
| Maximizar panel | Vista individual a pantalla completa |
| Edicion de URL/titulo | Desde el propio panel |
| Perfil persistente | Cookies y sesion conservadas entre ejecuciones |
| Atajos de teclado | `Ctrl+N` agregar, `F5` recargar, `F11` pantalla completa |

---

## Requisitos

- Python 3.8 o superior
- **CLI**: `requests` y `beautifulsoup4` (se instalan automaticamente)
- **UI**: `PyQt6` y `PyQt6-WebEngine` (se instalan automaticamente)
- Conexion a internet para la primera descarga de datos (CLI) o para cargar las webs (UI)

---

## Instalacion

### Linux y macOS

**Metodo 1: clonado manual**

```bash
git clone https://github.com/XONIDU/monitor-web.git
cd monitor-web
pip install -r requirements.txt   # opcional, start.py lo hace por ti
python start.py
```

**Metodo 2: comando `xoninstall` (recomendado para herramientas XONI)**

Anade la siguiente funcion a tu archivo `~/.bashrc`:

```bash
echo 'xoninstall() { if [ -z "$1" ]; then echo "Uso: xoninstall <repo>"; echo "Ej: xoninstall xoniran"; else git clone "https://github.com/XONIDU/$1.git"; fi; }' >> ~/.bashrc && source ~/.bashrc && echo "Listo. Usa: xoninstall monitor-web"
```

Despues, instala y ejecuta:

```bash
xoninstall monitor-web
cd monitor-web
python start.py
```

> La misma funcion permite instalar futuras herramientas de XONIDU, por ejemplo `xoninstall xoniran`.

### Windows

**Metodo 1: clonado manual (PowerShell o CMD)**

```cmd
git clone https://github.com/XONIDU/monitor-web.git
cd monitor-web
python start.py
```

**Metodo 2: lanzador `monitor_web.bat`**

Crea el archivo `monitor_web.bat` en el mismo directorio del proyecto:

```batch
@echo off
title MONITOR WEB 2026 - Lanzador
color 0A

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

cd /d "%~dp0"

if not exist "%~dp0start.py" (
    echo [ERROR] No se encuentra start.py en esta carpeta
    echo.
    pause
    exit /B
)

cls
echo ============================================================
echo           MONITOR WEB 2026 - Lanzador
echo ============================================================
echo.
echo [OK] Permisos de administrador obtenidos
echo.
echo [INFO] Directorio de trabajo: %~dp0
echo.
echo Iniciando MONITOR WEB...
echo.
echo [INFO] Podras elegir entre UI (grafica) o CLI (terminal)
echo.
echo ============================================================
echo.

python start.py

if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Ocurrio un error al ejecutar MONITOR WEB
    echo.
)

pause
```

Haz doble clic en `monitor_web.bat` para ejecutar el lanzador con permisos de administrador.

---

## Uso

### Linux/macOS

```bash
python start.py
```

### Windows

- Opcion 1: `python start.py` desde CMD o PowerShell
- Opcion 2: doble clic en `monitor_web.bat`

### Eleccion de modo

Al iniciar, `start.py` pregunta:

```
Selecciona el modo de ejecucion:
  1. UI  - Interfaz grafica (paneles web)
  2. CLI - Solo terminal y temperaturas
Elige (1/2) [1]:
```

- **UI**: se abre una ventana con los paneles web configurados.
- **CLI**: se inicia el monitor meteorologico con la Tierra animada.

---

## Configuracion

### Modo CLI — Clima

En la primera ejecucion se solicita:

1. Color del texto (0-9)
2. Una o varias ubicaciones (codigo postal + pais)
3. Modo de ejecucion (recurrente o unica vez; ambos en bucle infinito)

**Archivo de ubicaciones** (editable manualmente):

- Linux/macOS: `~/.xonichat/ubicaciones.txt`
- Windows: `%USERPROFILE%\.xonichat\ubicaciones.txt`

Formato: una ubicacion por linea, con codigo postal y pais separados por espacio.

```
28001 ES
55660 MX
75001 FR
```

**Cache de datos**: `~/.xonichat/weather_cache.json`  
Solo se descarga una vez; luego se reutiliza sin conexion.

### Modo UI — Paneles web

La configuracion se guarda en:

- Linux/macOS: `~/.config/monitor-web/config.json`
- Windows: `%USERPROFILE%\.config\monitor-web\config.json`

Incluye:

- Numero de columnas (0 = automatico)
- Lista de sitios: titulo, URL y minutos de refresco

Los paneles se gestionan desde la barra de herramientas y los botones de cada panel:

| Boton | Accion |
|-------|--------|
| R | Recargar |
| T | Configurar refresco automatico |
| E | Editar titulo / URL |
| M | Maximizar / restaurar |
| X | Quitar panel |

Atajos globales:

- `Ctrl+N`: agregar nueva web
- `F5`: recargar todos los paneles
- `F11`: pantalla completa

---

## Estructura del proyecto

| Archivo | Descripcion |
|---------|-------------|
| `start.py` | Lanzador universal; elige UI o CLI e instala dependencias |
| `monitor_ui.py` | Modo UI: paneles web en cuadricula |
| `monitor_cli.py` | Modo CLI: clima con animacion ASCII de la Tierra |
| `monitor_web.bat` | Lanzador para Windows (opcional) |
| `ubicaciones.txt` | `~/.xonichat/ubicaciones.txt` (CLI) |
| `weather_cache.json` | `~/.xonichat/weather_cache.json` (CLI) |
| `config.json` | `~/.config/monitor-web/config.json` (UI) |

---

## Pruebas

- CLI: `python monitor_cli.py`
- UI: `python monitor_ui.py`

Si ambos modos se ejecutan correctamente, la instalacion esta completa.

---

## Solucion de problemas

| Problema | Solucion |
|----------|----------|
| `No module named 'requests'` | `pip install requests beautifulsoup4` |
| `No module named 'PyQt6'` | `pip install PyQt6 PyQt6-WebEngine` |
| La animacion parpadea | Aumenta el tamano de la terminal (minimo 80x24) |
| No se muestran datos (CLI) | La primera ejecucion requiere conexion a internet |
| `Permission denied` en Linux | Ejecuta `python start.py` o aplica `chmod +x start.py` |
| Problemas de permisos en Windows | Usa `monitor_web.bat` |

---

## Licencia

**© 2026 Darian Alberto Camacho Salas (XONIDU)**  
Todos los derechos reservados. No se permite la copia, distribucion ni modificacion sin autorizacion expresa del autor.

---

## Contacto

- **Autor:** Darian Alberto Camacho Salas
- **Correo:** xonidu@gmail.com
- **GitHub:** [@XONIDU](https://github.com/XONIDU)

---

*Herramienta multiuso de terminal y escritorio para entusiastas de la meteorologia y la monitorizacion web.*
```