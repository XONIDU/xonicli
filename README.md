# 🌍 XONICLI

Cliente meteorológico por terminal con animación ASCII de la Tierra, optimizado para equipos de bajos recursos (ASUS Eee PC, Raspberry Pi, etc.)

## 📋 Características

- ✅ **Interfaz 100% terminal** – Rápida y ligera
- ✅ **Tierra animada girando** – Visualización continua junto a los datos
- ✅ **Múltiples ubicaciones** – Guarda varios códigos postales + país
- ✅ **Datos en caché** – Solo una descarga por internet (modo sin conexión después)
- ✅ **Secuencia automática** – Hoy, mañana, pasado mañana cada 10 segundos
- ✅ **Dos modos de ejecución** – Recurrente (bucle infinito) o consulta única
- ✅ **Gestor interactivo de ubicaciones** – Sin editar archivos manualmente
- ✅ **Sin `sudo`** – Las ubicaciones se guardan en `~/.xonichat/`

## 📦 Instalación

### Desde AUR (recomendado para Arch Linux)
```bash
yay -S xonicli
```

### Manual desde GitHub
```bash
git clone https://github.com/XONIDU/xonicli.git
cd xonicli
pip install -r requirements.txt
python start_weather.py   # o ./start_weather.py
```

## 🔑 Configuración

La primera vez que ejecutes `start_weather.py` se abrirá un gestor interactivo para añadir ubicaciones.

### ¿Dónde obtener los códigos postales?
Usa el código postal de tu ciudad (ej: `28001` para Madrid, `55660` para México).

### Ubicación manual del archivo
```
~/.xonichat/ubicaciones.txt   # Una ubicación por línea: CODIGO_PAIS
```
Formato del archivo:
```
28001 ES
55660 MX
75001 FR
```

## 🚀 Uso

```bash
xonicli
```
o si usas el lanzador:
```bash
start_weather.py
```

El programa te guiará para:
1. Seleccionar el color del texto (0-9)
2. Elegir una o varias ubicaciones
3. Seleccionar el modo de conexión:
   - **Recurrente** – Muestra el ciclo de días en bucle infinito hasta `Ctrl+C`
   - **Única vez** – Muestra el ciclo completo una sola vez y termina

### Ejemplo de sesión
```
$ xonicli

============================================================
   XONICLI - SISTEMA METEOROLOGICO CON TIERRA ANIMADA
============================================================
   Fuente: wttr.in | Sin emojis | Cache local
   La Tierra gira en tiempo real junto a los datos
============================================================

[SELECCIONA EL COLOR DEL TEXTO (0-9)]:
  0: Negro     1: Rojo     2: Verde     3: Amarillo
  4: Azul      5: Magenta  6: Cian      7: Blanco
  8: Gris      9: Rojo brillante
Numero [0-9] (Enter para blanco): 2

[UBICACIONES]
  1. Una sola ubicacion
  2. Varias ubicaciones
Elige (1/2): 1
Codigo de pais (ES, MX, AR, etc.): ES
Codigo postal: 28001

[MODO DE CONEXION]
  1. Tiempo real recurrente (bucle infinito, 10s entre cada dia)
  2. Una sola vez (muestra ciclo completo y termina)
Elige (1/2): 1

[INFO] Descargando desde internet (unica vez)...
Descargando 28001 ES ...
[OK] Datos guardados en cache.

  (Se muestra la Tierra girando junto a los datos climáticos)
```

## 📁 Estructura del paquete

| Archivo | Ubicación |
|---------|-----------|
| `xonicli` (o script principal) | `/usr/bin/xonicli` |
| `xonicli.py` | `/usr/share/xonicli/` |
| `ubicaciones.txt` | `~/.xonichat/ubicaciones.txt` |
| `weather_cache.json` (caché de datos) | `~/.xonichat/weather_cache.json` |
| `README.md` | `/usr/share/doc/xonicli/` |

## 🔄 Comportamiento detallado

- **Primera ejecución**: Descarga los datos meteorológicos de todas las ubicaciones y los guarda en caché.
- **Ejecuciones posteriores**: Lee el caché (sin usar internet) a menos que cambies las ubicaciones.
- **Animación continua**: La Tierra gira en la terminal mientras los datos se muestran a su lado (o debajo en terminales estrechas).
- **Secuencia**: Cada 10 segundos avanza al siguiente día (hoy → mañana → pasado mañana) y luego a la siguiente ubicación. En modo recurrente, al terminar todas las ubicaciones y días, comienza de nuevo desde el principio.

## 🧪 Pruebas

Ejecuta el script directamente:
```bash
python xonicli.py
```

## 🐛 Problemas comunes

| Problema | Solución |
|----------|----------|
| No se muestran datos | Verifica tu conexión a internet en la primera ejecución |
| Error `expected a nonnegative input` | Ya está corregido en la última versión |
| La animación parpadea | Ajusta el tamaño de la terminal (mínimo 80x24) |
| `No module 'requests'` | `pip install requests` |
| Error 404 o 400 | Confirma que el código postal y país sean correctos |

## 📄 Licencia

**© 2026 Darian Alberto Camacho Salas (XONIDU)**  
Todos los derechos reservados. No se permite copia, distribución o modificación sin autorización explícita.

## ✉️ Contacto

- **Creador**: Darian Alberto Camacho Salas
- **Email**: xonidu@gmail.com
- **GitHub**: [@XONIDU](https://github.com/XONIDU)

---
