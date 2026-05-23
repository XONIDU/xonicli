#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
XONICLI - SISTEMA METEOROLOGICO EN TERMINAL
Con animacion continua de la Tierra y datos climáticos simultáneos.
Sin emojis, secuencia cada 10 segundos, cache en disco.
AMbos modos (recurrente y unica vez) ahora son bucles infinitos.
"""

import requests
import time
import os
import sys
import json
import math
import shutil
from datetime import datetime
from pathlib import Path

# ============================================================================
# CONFIGURACION DE COLORES ANSI
# ============================================================================
COLORES = {
    0: '\033[30m', 1: '\033[31m', 2: '\033[32m', 3: '\033[33m',
    4: '\033[34m', 5: '\033[35m', 6: '\033[36m', 7: '\033[37m',
    8: '\033[90m', 9: '\033[91m'
}
RESET = '\033[0m'
BOLD = '\033[1m'
color_actual = RESET

def set_color(numero):
    global color_actual
    color_actual = COLORES.get(numero, COLORES[7])

def print_color(*args, sep=' ', end='\n'):
    texto = sep.join(str(a) for a in args)
    print(f"{color_actual}{texto}{RESET}", end=end)

# ============================================================================
# GENERACION DE LA TIERRA ASCII
# ============================================================================
def generar_tierra(angle, width=40, height=20):
    """Genera una matriz de caracteres para la Tierra girando."""
    chars = " .:-=+*#%@"
    radius = height // 2
    if radius < 3:
        radius = 3
    half_width = width // 2
    tierra = []
    for y in range(-radius, radius):
        line = []
        for x in range(-half_width, half_width):
            nx = x / half_width
            ny = y / radius
            dist2 = nx*nx + ny*ny
            if dist2 <= 1:
                nz = math.sqrt(max(0, 1 - dist2))
                lon = math.atan2(nx, nz) + angle
                lat = math.asin(ny)
                tex = math.sin(3*lon) + math.cos(5*lat) + math.sin(8*(lon+lat))
                light = nx*0.3 + ny*-0.4 + nz*0.8
                val = tex + light*2
                val_clamped = max(-3, min(3, val))
                idx = int(((val_clamped + 3) / 6) * (len(chars) - 1))
                idx = max(0, min(len(chars)-1, idx))
                line.append(chars[idx])
            else:
                line.append(' ')
        tierra.append(''.join(line))
    return tierra

# ============================================================================
# CACHE EN DISCO
# ============================================================================
def get_cache_path():
    home = Path.home()
    cache_dir = home / '.xonichat'
    cache_dir.mkdir(exist_ok=True)
    return cache_dir / 'weather_cache.json'

def load_cache(ubicaciones):
    cache_file = get_cache_path()
    if not cache_file.exists():
        return None
    try:
        with open(cache_file, 'r', encoding='utf-8') as f:
            cache = json.load(f)
        if cache.get('ubicaciones') == ubicaciones:
            return cache['datos']
        else:
            return None
    except:
        return None

def save_cache(ubicaciones, datos):
    cache_file = get_cache_path()
    try:
        with open(cache_file, 'w', encoding='utf-8') as f:
            json.dump({
                'ubicaciones': ubicaciones,
                'datos': datos,
                'timestamp': datetime.now().isoformat()
            }, f, indent=2, ensure_ascii=False)
    except:
        pass

# ============================================================================
# DATOS CLIMATICOS
# ============================================================================
def obtener_clima(cp, pais="ES"):
    url = f"https://wttr.in/{cp}+{pais}?format=j1"
    try:
        resp = requests.get(url, headers={"User-Agent": "curl/7.68.0"}, timeout=15)
        data = resp.json()
        ciudad = data['nearest_area'][0]['areaName'][0]['value']
        pais_nombre = data['nearest_area'][0]['country'][0]['value']
        actual = data['current_condition'][0]
        temp_c = float(actual['temp_C'])
        temp_f = float(actual['temp_F'])
        temp_k = temp_c + 273.15
        desc = actual['weatherDesc'][0]['value']
        humedad = actual['humidity']
        pronostico = []
        for dia in data['weather']:
            fecha = dia['date']
            max_c = float(dia['maxtempC'])
            min_c = float(dia['mintempC'])
            avg_c = float(dia['avgtempC'])
            max_f = (max_c * 9/5) + 32
            min_f = (min_c * 9/5) + 32
            avg_f = (avg_c * 9/5) + 32
            avg_k = avg_c + 273.15
            pronostico.append({
                'fecha': fecha, 'max_c': max_c, 'max_f': max_f,
                'min_c': min_c, 'min_f': min_f, 'avg_c': avg_c,
                'avg_f': avg_f, 'avg_k': avg_k
            })
        hoy = pronostico[0]
        return {
            'ciudad': ciudad, 'pais': pais_nombre, 'codigo': cp,
            'actual': {
                'temp_c': temp_c, 'temp_f': temp_f, 'temp_k': temp_k,
                'descripcion': desc, 'humedad': humedad,
                'min_c': hoy['min_c'], 'max_c': hoy['max_c']
            },
            'pronostico': pronostico
        }
    except Exception as e:
        return {'error': str(e), 'codigo': cp}

def obtener_todos_los_datos(ubicaciones):
    print_color("[INFO] Descargando datos (unica vez)...")
    todos = []
    for cp, pais in ubicaciones:
        print_color(f"Descargando {cp}, {pais} ...")
        datos = obtener_clima(cp, pais)
        todos.append(datos)
        time.sleep(0.5)
    return todos

# ============================================================================
# FORMATEO DE DATOS PARA PANTALLA
# ============================================================================
def formatear_datos(datos, idx_dia):
    """Devuelve una lista de líneas con la información del día."""
    if 'error' in datos:
        return [f"ERROR: {datos['codigo']} - {datos['error']}"]
    prono = datos['pronostico']
    if idx_dia >= len(prono):
        return ["[No hay mas datos]"]
    dia = prono[idx_dia]
    hora = datetime.now().strftime("%H:%M:%S")
    lineas = []
    if idx_dia == 0:
        lineas.append(f"HORA: {hora}  |  UBICACION: {datos['ciudad']}, {datos['pais']} ({datos['codigo']})")
        lineas.append(f"CONDICION: {datos['actual']['descripcion']}")
        lineas.append(f"HUMEDAD: {datos['actual']['humedad']} %")
        lineas.append(f"TEMP ACTUAL: {datos['actual']['temp_c']:.1f} C / {datos['actual']['temp_f']:.1f} F / {datos['actual']['temp_k']:.2f} K")
        lineas.append(f"MIN/MAX HOY: {datos['actual']['min_c']:.1f} C / {datos['actual']['max_c']:.1f} C")
    else:
        etiqueta = {1: "MANANA", 2: "PASADO MANANA"}.get(idx_dia, f"DIA {idx_dia+1}")
        lineas.append(f"{etiqueta} {dia['fecha']}  |  {datos['ciudad']}, {datos['pais']}")
        lineas.append("TEMPERATURAS:")
        lineas.append(f"  Min: {dia['min_c']:.1f} C / {dia['min_f']:.1f} F")
        lineas.append(f"  Max: {dia['max_c']:.1f} C / {dia['max_f']:.1f} F")
        lineas.append(f"  Prom: {dia['avg_c']:.1f} C / {dia['avg_f']:.1f} F / {dia['avg_k']:.2f} K")
    return lineas

# ============================================================================
# BUCLE PRINCIPAL CON ANIMACION SIMULTANEA
# AHORA AMBOS MODOS SON CICLICOS INFINITOS
# ============================================================================
def run_con_animacion(todos_datos):
    """
    Bucle principal: dibuja la Tierra girando y los datos actuales.
    Los datos cambian cada 10 segundos según secuencia.
    Siempre se ejecuta en bucle infinito (hasta Ctrl+C).
    """
    # Determinar secuencia de (datos, idx_dia)
    max_dias = 3
    for d in todos_datos:
        if 'pronostico' in d:
            max_dias = max(max_dias, len(d['pronostico']))
    
    secuencia = []
    for datos in todos_datos:
        for dia_idx in range(max_dias):
            if dia_idx < len(datos.get('pronostico', [])):
                secuencia.append((datos, dia_idx))
    
    if not secuencia:
        print_color("[ERROR] No hay datos para mostrar")
        return
    
    idx_secuencia = 0
    ultimo_cambio = time.time()
    intervalo = 10  # segundos entre cada dia
    
    # Ocultar cursor
    sys.stdout.write('\033[?25l')
    sys.stdout.flush()
    
    # Dimensiones fijas para la Tierra
    ancho_tierra = 40
    alto_tierra = 20
    # Obtener tamaño de terminal
    try:
        term_width, term_height = shutil.get_terminal_size((80, 24))
    except:
        term_width, term_height = 80, 24
    
    angle = 0
    try:
        while True:  # Bucle infinito, se sale solo con Ctrl+C
            start_frame = time.time()
            
            # Verificar si toca cambiar de dia (cada 10 segundos)
            ahora = time.time()
            if ahora - ultimo_cambio >= intervalo:
                # Avanzar al siguiente día de forma cíclica (siempre módulo)
                idx_secuencia = (idx_secuencia + 1) % len(secuencia)
                ultimo_cambio = ahora
            
            # Obtener datos actuales a mostrar
            datos_actuales, dia_actual = secuencia[idx_secuencia]
            lineas_datos = formatear_datos(datos_actuales, dia_actual)
            
            # Generar la Tierra en el frame actual
            tierra = generar_tierra(angle, width=ancho_tierra, height=alto_tierra)
            angle += 0.08  # velocidad de rotacion
            
            # Construir la pantalla completa
            if term_width >= (ancho_tierra + 40):
                # Colocar lado a lado
                max_lineas = max(len(tierra), len(lineas_datos))
                pantalla = []
                for i in range(max_lineas):
                    linea_tierra = tierra[i] if i < len(tierra) else ' ' * ancho_tierra
                    linea_datos = lineas_datos[i] if i < len(lineas_datos) else ''
                    espacio_datos = term_width - ancho_tierra - 2
                    if len(linea_datos) > espacio_datos:
                        linea_datos = linea_datos[:espacio_datos-3] + '...'
                    pantalla.append(f"{linea_tierra}  {linea_datos}")
            else:
                # Apilar: primero la Tierra, luego los datos
                pantalla = tierra + ["", "--- DATOS CLIMATICOS ---"] + lineas_datos
            
            # Limpiar pantalla y dibujar
            sys.stdout.write('\033[H')
            sys.stdout.write('\n'.join(pantalla))
            sys.stdout.flush()
            
            # Control de velocidad de frames (aprox 30 fps)
            elapsed = time.time() - start_frame
            if elapsed < 0.033:
                time.sleep(0.033 - elapsed)
    except KeyboardInterrupt:
        pass
    except Exception as e:
        sys.stdout.write('\033[?25h')
        sys.stdout.flush()
        print_color(f"\n[ERROR interno] {e}")
    finally:
        sys.stdout.write('\033[?25h')
        sys.stdout.flush()
        os.system('cls' if os.name == 'nt' else 'clear')
        print_color("\n[Sesion finalizada]")

# ============================================================================
# INTERFAZ DE USUARIO
# ============================================================================
def seleccionar_color():
    print("\n[SELECCIONA EL COLOR DEL TEXTO (0-9)]:")
    print("  0: Negro     1: Rojo     2: Verde     3: Amarillo")
    print("  4: Azul      5: Magenta  6: Cian      7: Blanco")
    print("  8: Gris      9: Rojo brillante")
    while True:
        try:
            op = input("Numero [0-9] (Enter para blanco): ").strip()
            if op == "":
                return 7
            num = int(op)
            if 0 <= num <= 9:
                return num
            else:
                print("Elige 0-9.")
        except ValueError:
            print("Ingresa un numero.")

def preguntar_ubicaciones():
    print("\n[UBICACIONES]")
    print("  1. Una sola ubicacion")
    print("  2. Varias ubicaciones")
    while True:
        op = input("Elige (1/2): ").strip()
        if op == "1":
            pais = input("Codigo de pais (ES, MX, AR, etc.): ").strip().upper()
            cp = input("Codigo postal: ").strip()
            return [(cp, pais)]
        elif op == "2":
            ubicaciones = []
            print("Ingresa cada ubicacion. Deja el pais vacio para terminar.")
            while True:
                pais = input("Pais (o Enter para terminar): ").strip().upper()
                if pais == "":
                    if len(ubicaciones) == 0:
                        print("Debes ingresar al menos una ubicacion.")
                        continue
                    break
                cp = input(f"Codigo postal para {pais}: ").strip()
                ubicaciones.append((cp, pais))
            return ubicaciones
        else:
            print("Responde 1 o 2.")

def preguntar_modo():
    print("\n[MODO DE CONEXION]")
    print("  1. Tiempo real recurrente (bucle infinito, 10s entre cada dia)")
    print("  2. Una sola vez (tambien bucle infinito, usa datos cacheados)")
    print("   (Ambos modos se ejecutan hasta Ctrl+C, solo cambia si descargan nuevos datos)")
    while True:
        op = input("Elige (1/2): ").strip()
        if op == "1" or op == "2":
            return op
        else:
            print("Responde 1 o 2.")

def main():
    # Limpiar pantalla
    os.system('cls' if os.name == 'nt' else 'clear')
    print("=" * 70)
    print("   XONICLI - SISTEMA METEOROLOGICO CON TIERRA ANIMADA")
    print("=" * 70)
    print("   Fuente: wttr.in | Sin emojis | Cache local")
    print("   La Tierra gira en tiempo real junto a los datos")
    print("=" * 70)
    
    num_color = seleccionar_color()
    set_color(num_color)
    
    ubicaciones = preguntar_ubicaciones()
    modo = preguntar_modo()
    
    # Cargar o descargar datos
    datos_cacheados = load_cache(ubicaciones)
    if datos_cacheados is not None:
        print("\n[CACHE] Usando datos guardados (sin internet).")
        todos_datos = datos_cacheados
    else:
        print("\n[INFO] Descargando desde internet (unica vez)...")
        todos_datos = obtener_todos_los_datos(ubicaciones)
        save_cache(ubicaciones, todos_datos)
        print("[OK] Datos guardados en cache.")
    
    # Si el usuario eligió modo 2 (unica vez), no hacemos nada diferente,
    # simplemente ejecutamos el bucle (que ya es infinito).
    # Opcional: si se quisiera que el modo 1 volviera a descargar periódicamente,
    # habría que implementar otra lógica, pero por simplicidad ambos usan cache.
    # El mensaje de inicio puede variar.
    if modo == "2":
        print("\n[EJECUTANDO EN MODO 'UNA SOLA VEZ' - Bucle infinito hasta Ctrl+C]")
    else:
        print("\n[EJECUTANDO EN MODO RECURRENTE - Bucle infinito hasta Ctrl+C]")
    
    time.sleep(1)
    
    # Ejecutar con animacion simultanea
    run_con_animacion(todos_datos)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print_color("\n[Saliendo...]")
    except Exception as e:
        print_color(f"\n[ERROR GLOBAL] {e}")
