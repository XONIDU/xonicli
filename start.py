#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
XONICLI 2026 - Lanzador Universal con Gestor de Ubicaciones
Sistema Meteorológico en Terminal con animación de la Tierra
Desarrollador: Darian Alberto Camacho Salas
Organización: XONIDU
"""

import subprocess
import sys
import os
import platform
import shutil
import time
from pathlib import Path

# ============================================================================
# Colores para terminal
# ============================================================================
class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    END = '\033[0m'
    BOLD = '\033[1m'
    
    @staticmethod
    def supports_color():
        if platform.system() == 'Windows':
            try:
                import ctypes
                kernel32 = ctypes.windll.kernel32
                return kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
            except:
                return False
        return True

if not Colors.supports_color():
    for attr in dir(Colors):
        if not attr.startswith('_') and attr != 'supports_color':
            setattr(Colors, attr, '')

# ============================================================================
# Detección del sistema
# ============================================================================
def get_system():
    return platform.system().lower()

def get_linux_distro():
    if get_system() != 'linux':
        return None
    try:
        if os.path.exists('/etc/os-release'):
            with open('/etc/os-release', 'r') as f:
                content = f.read().lower()
                if 'ubuntu' in content or 'debian' in content or 'mint' in content or 'antix' in content:
                    return 'debian-based'
                elif 'arch' in content or 'manjaro' in content:
                    return 'arch-based'
                elif 'fedora' in content:
                    return 'fedora'
                elif 'centos' in content or 'rhel' in content:
                    return 'centos'
                elif 'opensuse' in content:
                    return 'opensuse'
        if shutil.which('apt'):
            return 'debian-based'
        elif shutil.which('pacman'):
            return 'arch-based'
        elif shutil.which('dnf'):
            return 'fedora'
        elif shutil.which('yum'):
            return 'centos'
        elif shutil.which('zypper'):
            return 'opensuse'
        return 'linux-generico'
    except:
        return 'linux-generico'

def get_python_command():
    if get_system() == 'windows':
        return ['python']
    else:
        try:
            subprocess.run(['python3', '--version'], capture_output=True, check=True)
            return ['python3']
        except:
            return ['python']

def get_pip_command():
    return [sys.executable, '-m', 'pip']

def get_install_flags():
    flags = []
    sistema = get_system()
    distro = get_linux_distro()
    if sistema == 'linux':
        if distro in ['arch-based', 'fedora']:
            flags.append('--break-system-packages')
        else:
            flags.append('--user')
    elif sistema == 'darwin':
        flags.append('--user')
    return flags

def get_script_dir():
    return os.path.dirname(os.path.abspath(__file__))

def get_xonicli_path():
    """Detecta la ruta de xonicli.py en múltiples ubicaciones"""
    script_dir = get_script_dir()
    rutas = [
        os.path.join(script_dir, 'xonicli.py'),
        '/usr/share/xonicli/xonicli.py',
        os.path.join(os.path.expanduser("~"), '.xonichat', 'xonicli.py'),
        os.path.join(os.getcwd(), 'xonicli.py')
    ]
    for r in rutas:
        if os.path.exists(r):
            return r
    return None

def print_banner():
    sistema = get_system()
    distro = get_linux_distro()
    sistema_texto = {
        'windows': 'WINDOWS',
        'linux': f'LINUX ({distro.upper()})' if distro else 'LINUX',
        'darwin': 'MACOS'
    }.get(sistema, 'DESCONOCIDO')
    
    banner = f"""
{Colors.PURPLE}{Colors.BOLD}╔══════════════════════════════════════════════════════════╗
║                    XONICLI 2026 v1.0                         ║
║              Sistema Meteorológico en Terminal                ║
║                   Optimizado para 1GB RAM                     ║
║                Con animación ASCII de la Tierra               ║
║                                                            ║
║               Sistema detectado: {sistema_texto:<27} ║
║                                                            ║
║               Desarrollado por: Darian Alberto             ║
║                      Camacho Salas                         ║
║                      Organización: XONIDU                  ║
╚══════════════════════════════════════════════════════════════╝{Colors.END}
    """
    print(banner)

def mostrar_ayuda():
    ayuda = f"""
{Colors.BOLD}USO DE XONICLI:{Colors.END}

  xonicli

{Colors.BOLD}CARACTERISTICAS:{Colors.END}

  ✅ Interfaz 100% terminal con Tierra animada
  ✅ Múltiples ubicaciones (país + código postal)
  ✅ Datos en caché (solo una descarga por internet)
  ✅ Secuencia automática: hoy, mañana, pasado mañana
  ✅ Dos modos: recurrente (bucle) o única consulta

{Colors.BOLD}COMANDOS DENTRO DEL PROGRAMA:{Colors.END}

  Ctrl+C     - Salir del programa

{Colors.BOLD}OBTENER CÓDIGOS POSTALES:{Colors.END}

  Introduce el código postal de tu ciudad.
  Ejemplo: 28001 (Madrid, España), 55660 (México)
    """
    print(ayuda)

# ============================================================================
# Gestión de ubicaciones (similar a gestión de keys)
# ============================================================================
def get_ubicaciones_path():
    """Devuelve la ruta del archivo de ubicaciones"""
    home_ubic = os.path.join(os.path.expanduser("~"), '.xonichat', 'ubicaciones.txt')
    return home_ubic

def gestionar_ubicaciones():
    """Gestión interactiva de ubicaciones (país + código postal)"""
    ubic_path = get_ubicaciones_path()
    ubic_dir = os.path.dirname(ubic_path)
    
    if not os.path.exists(ubic_dir):
        os.makedirs(ubic_dir, exist_ok=True)
    
    if not os.path.exists(ubic_path):
        with open(ubic_path, 'w') as f:
            f.write("# Archivo de ubicaciones para XONICLI\n")
            f.write("# Formato: CODIGO_POSTAL PAIS (ej: 28001 ES)\n")
            f.write("# Cada línea una ubicación\n\n")
            f.write("# Ejemplo:\n")
            f.write("# 28001 ES\n")
            f.write("# 55660 MX\n")
    
    # Leer ubicaciones actuales
    ubicaciones = []
    with open(ubic_path, 'r') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#'):
                partes = line.split()
                if len(partes) >= 2:
                    cp = partes[0]
                    pais = partes[1].upper()
                    ubicaciones.append((cp, pais))
    
    print(f"\n{Colors.CYAN}{Colors.BOLD}=== GESTOR DE UBICACIONES ==={Colors.END}")
    print(f"📁 Archivo: {ubic_path}")
    print(f"📍 Ubicaciones activas: {len(ubicaciones)}")
    
    if ubicaciones:
        print(f"\n{Colors.BOLD}Ubicaciones actuales:{Colors.END}")
        for i, (cp, pais) in enumerate(ubicaciones, 1):
            print(f"  {i}. {cp} ({pais})")
    
    print(f"\n{Colors.BOLD}Opciones:{Colors.END}")
    print("  1. Agregar nueva ubicación")
    print("  2. Eliminar una ubicación")
    print("  3. Salir (continuar con las ubicaciones actuales)")
    
    opcion = input(f"\n{Colors.YELLOW}Elige una opción (1-3): {Colors.END}").strip()
    
    if opcion == '1':
        cp = input(f"{Colors.CYAN}Código postal: {Colors.END}").strip()
        pais = input(f"{Colors.CYAN}Código de país (ES, MX, AR, etc.): {Colors.END}").strip().upper()
        if cp and pais:
            with open(ubic_path, 'a') as f:
                f.write(f"{cp} {pais}\n")
            print(f"{Colors.GREEN}✅ Ubicación agregada correctamente{Colors.END}")
            time.sleep(1)
        else:
            print(f"{Colors.RED}❌ Datos inválidos{Colors.END}")
            time.sleep(1)
    
    elif opcion == '2':
        if not ubicaciones:
            print(f"{Colors.YELLOW}⚠️ No hay ubicaciones para eliminar{Colors.END}")
            time.sleep(1)
        else:
            print(f"\n{Colors.BOLD}Selecciona la ubicación a eliminar:{Colors.END}")
            for i, (cp, pais) in enumerate(ubicaciones, 1):
                print(f"  {i}. {cp} ({pais})")
            try:
                eliminar = int(input(f"{Colors.YELLOW}Número a eliminar (0 = cancelar): {Colors.END}"))
                if 1 <= eliminar <= len(ubicaciones):
                    ubicaciones.pop(eliminar - 1)
                    with open(ubic_path, 'w') as f:
                        f.write("# Archivo de ubicaciones para XONICLI\n")
                        f.write("# Formato: CODIGO_POSTAL PAIS (ej: 28001 ES)\n")
                        f.write("# Cada línea una ubicación\n\n")
                        for cp, pais in ubicaciones:
                            f.write(f"{cp} {pais}\n")
                    print(f"{Colors.GREEN}✅ Ubicación eliminada correctamente{Colors.END}")
                    time.sleep(1)
                elif eliminar == 0:
                    print(f"{Colors.YELLOW}Operación cancelada{Colors.END}")
                else:
                    print(f"{Colors.RED}❌ Número inválido{Colors.END}")
            except ValueError:
                print(f"{Colors.RED}❌ Entrada inválida{Colors.END}")
    
    print(f"{Colors.GREEN}✅ Continuando con {len(ubicaciones)} ubicación(es)...{Colors.END}")
    return ubic_path

# ============================================================================
# Verificación de dependencias (similar a XONICHAT)
# ============================================================================
def check_python():
    try:
        cmd = get_python_command() + ['--version']
        subprocess.run(cmd, capture_output=True, check=True)
        return True
    except:
        return False

def check_pip():
    try:
        cmd = get_pip_command() + ['--version']
        subprocess.run(cmd, capture_output=True, check=True)
        return True
    except:
        return False

def install_pip_linux():
    distro = get_linux_distro()
    print(f"{Colors.YELLOW}Instalando pip en Linux ({distro})...{Colors.END}")
    if distro == 'debian-based':
        try:
            subprocess.run(['sudo', 'apt', 'update'], check=False)
            subprocess.run(['sudo', 'apt', 'install', '-y', 'python3-pip'], check=True)
            return True
        except:
            return False
    elif distro == 'arch-based':
        try:
            subprocess.run(['sudo', 'pacman', '-S', '--noconfirm', 'python-pip'], check=True)
            return True
        except:
            return False
    return False

def install_pip_windows():
    print(f"{Colors.YELLOW}Instalando pip en Windows...{Colors.END}")
    try:
        subprocess.run([sys.executable, '-m', 'ensurepip', '--upgrade'], check=True)
        return True
    except:
        return False

def check_requests():
    try:
        __import__('requests')
        return True
    except ImportError:
        return False

def install_requests():
    print(f"{Colors.YELLOW}Instalando requests...{Colors.END}")
    if not check_pip():
        return False
    flags = get_install_flags()
    try:
        cmd = get_pip_command() + ['install', 'requests'] + flags
        subprocess.run(cmd, check=True, capture_output=True)
        print(f"{Colors.GREEN}requests instalado correctamente.{Colors.END}")
        return True
    except:
        try:
            cmd = get_pip_command() + ['install', 'requests']
            subprocess.run(cmd, check=True)
            print(f"{Colors.GREEN}requests instalado correctamente.{Colors.END}")
            return True
        except:
            return False

# ============================================================================
# Función principal
# ============================================================================
def main():
    if get_system() == 'windows':
        os.system('cls')
    else:
        os.system('clear')
    
    print_banner()
    
    if len(sys.argv) > 1 and sys.argv[1] in ['-h', '--help', '/?']:
        mostrar_ayuda()
        if get_system() != 'windows':
            input(f"\n{Colors.YELLOW}Presiona Enter para salir...{Colors.END}")
        return
    
    if not check_python():
        print(f"\n{Colors.RED}❌ Python no está instalado{Colors.END}")
        sys.exit(1)
    
    ver_py = subprocess.run(get_python_command() + ['--version'], capture_output=True, text=True).stdout.strip()
    print(f"{Colors.BOLD}Python:{Colors.END} {ver_py}")
    
    if not check_pip():
        print(f"\n{Colors.YELLOW}⚠️ Pip no encontrado. Instalando...{Colors.END}")
        sistema = get_system()
        if sistema == 'linux':
            if not install_pip_linux():
                print(f"{Colors.RED}No se pudo instalar pip.{Colors.END}")
                sys.exit(1)
        elif sistema == 'windows':
            if not install_pip_windows():
                print(f"{Colors.RED}No se pudo instalar pip.{Colors.END}")
                sys.exit(1)
    else:
        print(f"{Colors.GREEN}✓ Pip disponible{Colors.END}")
    
    if not check_requests():
        print(f"\n{Colors.YELLOW}⚠️ requests no encontrado. Instalando...{Colors.END}")
        if not install_requests():
            print(f"{Colors.RED}No se pudo instalar requests.{Colors.END}")
            sys.exit(1)
    else:
        print(f"{Colors.GREEN}✓ requests disponible{Colors.END}")
    
    # Gestionar ubicaciones
    gestionar_ubicaciones()
    
    # Buscar el script principal xonicli.py
    ruta_xonicli = get_xonicli_path()
    if not ruta_xonicli:
        print(f"\n{Colors.RED}❌ No se encuentra xonicli.py{Colors.END}")
        print(f"{Colors.YELLOW}Asegúrate de que xonicli.py esté en el mismo directorio que este lanzador.{Colors.END}")
        sys.exit(1)
    
    xonicli_dir = os.path.dirname(ruta_xonicli)
    print(f"{Colors.GREEN}✓ xonicli.py encontrado en: {xonicli_dir}{Colors.END}")
    
    # Cambiar al directorio y ejecutar
    os.chdir(xonicli_dir)
    print(f"\n{Colors.BOLD}🌍 Iniciando XONICLI...{Colors.END}")
    print(f"{Colors.CYAN}Para salir: presiona Ctrl+C en cualquier momento{Colors.END}")
    print("-"*50)
    
    try:
        python_cmd = get_python_command()
        subprocess.run(python_cmd + [ruta_xonicli])
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}🛑 Programa detenido por el usuario.{Colors.END}")
    except Exception as e:
        print(f"\n{Colors.RED}❌ Error: {e}{Colors.END}")
    
    print(f"\n{Colors.GREEN}Gracias por usar XONICLI{Colors.END}")
    if get_system() != 'windows':
        input(f"{Colors.YELLOW}Presiona Enter para salir...{Colors.END}")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}Saliendo...{Colors.END}")
    except Exception as e:
        print(f"\n{Colors.RED}Error inesperado: {e}{Colors.END}")
