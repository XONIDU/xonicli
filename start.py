#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
MONITOR WEB 2026 - Lanzador Universal
Permite elegir entre interfaz grafica (UI) o terminal (CLI).
Verifica dependencias, instala PyQt6 y requests segun sea necesario.
Compatible con Windows, Linux (varias distros) y macOS.
Desarrollador: Darian Alberto Camacho Salas
Organizacion: XONIDU
"""

import subprocess
import sys
import os
import platform
import shutil
import time

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
            except Exception:
                return False
        return True

if not Colors.supports_color():
    for attr in dir(Colors):
        if not attr.startswith('_') and attr != 'supports_color':
            setattr(Colors, attr, '')

# ============================================================================
# Deteccion del sistema
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
                if any(x in content for x in ['ubuntu', 'debian', 'mint', 'antix', 'pop!_os']):
                    return 'debian-based'
                elif any(x in content for x in ['arch', 'manjaro', 'endeavouros']):
                    return 'arch-based'
                elif 'fedora' in content:
                    return 'fedora'
                elif any(x in content for x in ['centos', 'rhel', 'rocky', 'almalinux']):
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
    except Exception:
        return 'linux-generico'

def get_python_command():
    if get_system() == 'windows':
        return ['python']
    try:
        subprocess.run(['python3', '--version'], capture_output=True, check=True)
        return ['python3']
    except Exception:
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

def get_script_path(name):
    """Busca un script en el directorio actual o rutas comunes."""
    script_dir = get_script_dir()
    rutas = [
        os.path.join(script_dir, name),
        f'/usr/share/monitor-web/{name}',
        os.path.join(os.path.expanduser("~"), '.monitor-web', name),
        os.path.join(os.getcwd(), name),
    ]
    for r in rutas:
        if os.path.exists(r):
            return r
    return None

# ============================================================================
# Banner
# ============================================================================
def print_banner():
    sistema = get_system()
    distro = get_linux_distro()
    sistema_texto = {
        'windows': 'WINDOWS',
        'linux': f'LINUX ({distro.upper()})' if distro else 'LINUX',
        'darwin': 'MACOS'
    }.get(sistema, 'DESCONOCIDO')

    banner = f"""
{Colors.PURPLE}{Colors.BOLD}============================================================
                  MONITOR WEB 2026
            Visualiza varias webs a la vez
                   Optimizado para 1GB RAM

               Sistema detectado: {sistema_texto:<27}
               Desarrollado por: Darian Alberto
                      Camacho Salas
                      Organizacion: XONIDU
============================================================{Colors.END}
    """
    print(banner)

def mostrar_ayuda():
    ayuda = f"""
{Colors.BOLD}USO DE MONITOR WEB:{Colors.END}

  python start.py

{Colors.BOLD}MODOS DISPONIBLES:{Colors.END}

  1. UI  - Interfaz grafica con paneles web (requiere PyQt6)
  2. CLI - Solo terminal, muestra temperaturas

{Colors.BOLD}CONTROLES EN UI:{Colors.END}

  Ctrl+N     - Agregar nueva web
  F5         - Recargar todos los paneles
  F11        - Pantalla completa
  Botones de cada panel: recargar, refresco, editar, maximizar, cerrar

{Colors.BOLD}CONTROLES EN CLI:{Colors.END}

  Ctrl+C     - Salir del programa
  Las webs se muestran en secuencia, refrescandose cada 30 segundos
    """
    print(ayuda)

# ============================================================================
# Verificacion e instalacion de dependencias
# ============================================================================
def check_python():
    try:
        cmd = get_python_command() + ['--version']
        subprocess.run(cmd, capture_output=True, check=True)
        return True
    except Exception:
        return False

def check_pip():
    try:
        cmd = get_pip_command() + ['--version']
        subprocess.run(cmd, capture_output=True, check=True)
        return True
    except Exception:
        return False

def install_pip_linux():
    distro = get_linux_distro()
    print(f"{Colors.YELLOW}Instalando pip en Linux ({distro})...{Colors.END}")
    if distro == 'debian-based':
        try:
            subprocess.run(['sudo', 'apt', 'update'], check=False)
            subprocess.run(['sudo', 'apt', 'install', '-y', 'python3-pip'], check=True)
            return True
        except Exception:
            return False
    elif distro == 'arch-based':
        try:
            subprocess.run(['sudo', 'pacman', '-S', '--noconfirm', 'python-pip'], check=True)
            return True
        except Exception:
            return False
    elif distro == 'fedora':
        try:
            subprocess.run(['sudo', 'dnf', 'install', '-y', 'python3-pip'], check=True)
            return True
        except Exception:
            return False
    elif distro == 'centos':
        try:
            subprocess.run(['sudo', 'yum', 'install', '-y', 'python3-pip'], check=True)
            return True
        except Exception:
            return False
    elif distro == 'opensuse':
        try:
            subprocess.run(['sudo', 'zypper', 'install', '-y', 'python3-pip'], check=True)
            return True
        except Exception:
            return False
    return False

def install_pip_windows():
    print(f"{Colors.YELLOW}Instalando pip en Windows...{Colors.END}")
    try:
        subprocess.run([sys.executable, '-m', 'ensurepip', '--upgrade'], check=True)
        return True
    except Exception:
        return False

def check_module(name):
    try:
        __import__(name)
        return True
    except ImportError:
        return False

def install_packages(packages):
    """Instala una lista de paquetes con pip, probando flags."""
    if not check_pip():
        return False
    flags = get_install_flags()
    try:
        cmd = get_pip_command() + ['install'] + packages + flags
        subprocess.run(cmd, check=True)
        return True
    except Exception:
        pass
    try:
        cmd = get_pip_command() + ['install'] + packages
        subprocess.run(cmd, check=True)
        return True
    except Exception:
        return False

def ensure_ui_dependencies():
    """Verifica e instala PyQt6 y PyQt6-WebEngine."""
    if check_module('PyQt6.QtWidgets') and check_module('PyQt6.QtWebEngineWidgets'):
        print(f"{Colors.GREEN}[OK] PyQt6 disponible{Colors.END}")
        return True
    print(f"{Colors.YELLOW}[WARN] PyQt6 no encontrado. Instalando...{Colors.END}")
    ok = install_packages(['PyQt6', 'PyQt6-WebEngine'])
    if ok:
        print(f"{Colors.GREEN}PyQt6 instalado correctamente.{Colors.END}")
    return ok

def ensure_cli_dependencies():
    """Verifica e instala requests y beautifulsoup4."""
    need = []
    if not check_module('requests'):
        need.append('requests')
    if not check_module('bs4'):
        need.append('beautifulsoup4')
    if not need:
        print(f"{Colors.GREEN}[OK] Dependencias CLI disponibles{Colors.END}")
        return True
    print(f"{Colors.YELLOW}[WARN] Faltan dependencias CLI: {', '.join(need)}. Instalando...{Colors.END}")
    ok = install_packages(need)
    if ok:
        print(f"{Colors.GREEN}Dependencias CLI instaladas.{Colors.END}")
    return ok

# ============================================================================
# Funcion principal
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
        print(f"\n{Colors.RED}[ERROR] Python no esta instalado{Colors.END}")
        sys.exit(1)

    ver_py = subprocess.run(get_python_command() + ['--version'],
                            capture_output=True, text=True).stdout.strip()
    print(f"{Colors.BOLD}Python:{Colors.END} {ver_py}")

    if not check_pip():
        print(f"\n{Colors.YELLOW}[WARN] Pip no encontrado. Instalando...{Colors.END}")
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
            print(f"{Colors.RED}Instala pip manualmente para {sistema}.{Colors.END}")
            sys.exit(1)
    else:
        print(f"{Colors.GREEN}[OK] Pip disponible{Colors.END}")

    # Elegir modo
    print(f"\n{Colors.BOLD}Selecciona el modo de ejecucion:{Colors.END}")
    print("  1. UI  - Interfaz grafica (paneles web)")
    print("  2. CLI - Solo terminal y temperaturas")
    opcion = input(f"{Colors.YELLOW}Elige (1/2) [1]: {Colors.END}").strip() or "1"

    if opcion == "1":
        # Modo UI
        if not ensure_ui_dependencies():
            print(f"{Colors.RED}No se pudieron instalar las dependencias de UI.{Colors.END}")
            sys.exit(1)
        ruta = get_script_path('monitor_ui.py')
        if not ruta:
            print(f"{Colors.RED}[ERROR] No se encuentra monitor_ui.py{Colors.END}")
            sys.exit(1)
        print(f"{Colors.GREEN}[OK] monitor_ui.py encontrado en: {os.path.dirname(ruta)}{Colors.END}")
        os.chdir(os.path.dirname(ruta))
        print(f"\n{Colors.BOLD}Iniciando MONITOR WEB (UI)...{Colors.END}")
        print(f"{Colors.CYAN}Para salir: cierra la ventana o Ctrl+C{Colors.END}")
        print("-" * 50)
        try:
            subprocess.run(get_python_command() + [ruta])
        except KeyboardInterrupt:
            print(f"\n{Colors.YELLOW}Programa detenido por el usuario.{Colors.END}")
        except Exception as e:
            print(f"\n{Colors.RED}Error: {e}{Colors.END}")
    else:
        # Modo CLI
        if not ensure_cli_dependencies():
            print(f"{Colors.RED}No se pudieron instalar las dependencias CLI.{Colors.END}")
            sys.exit(1)
        ruta = get_script_path('monitor_cli.py')
        if not ruta:
            print(f"{Colors.RED}[ERROR] No se encuentra monitor_cli.py{Colors.END}")
            sys.exit(1)
        print(f"{Colors.GREEN}[OK] monitor_cli.py encontrado en: {os.path.dirname(ruta)}{Colors.END}")
        os.chdir(os.path.dirname(ruta))
        print(f"\n{Colors.BOLD}Iniciando MONITOR WEB (CLI)...{Colors.END}")
        print(f"{Colors.CYAN}Para salir: Ctrl+C{Colors.END}")
        print("-" * 50)
        try:
            subprocess.run(get_python_command() + [ruta])
        except KeyboardInterrupt:
            print(f"\n{Colors.YELLOW}Programa detenido por el usuario.{Colors.END}")
        except Exception as e:
            print(f"\n{Colors.RED}Error: {e}{Colors.END}")

    print(f"\n{Colors.GREEN}Gracias por usar MONITOR WEB{Colors.END}")
    if get_system() != 'windows':
        input(f"{Colors.YELLOW}Presiona Enter para salir...{Colors.END}")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}Saliendo...{Colors.END}")
    except Exception as e:
        print(f"\n{Colors.RED}Error inesperado: {e}{Colors.END}")
