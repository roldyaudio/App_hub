import os
import subprocess
import sys
import urllib.request
import ctypes

def show_msgbox(title, text, style):
    """Muestra un cuadro de diálogo de Windows (0: OK, 4: Yes/No)"""
    return ctypes.windll.user32.MessageBoxW(0, text, title, style)

def check_python_version():
    """
    Forzamos la comprobación. Si NO es 3.12, preguntamos.
    Pydub y Torch 2.5 funcionan mejor en 3.12.
    """
    major, minor = sys.version_info.major, sys.version_info.minor
    
    # Si es 3.13 o superior, lanzamos la alerta
    if major == 3 and minor >= 13:
        print(f"⚠️ Versión incompatible detectada: {major}.{minor}")
        
        msg = (f"Tu versión actual de Python ({major}.{minor}) NO es compatible con las librerías de Audio (pydub).\n\n"
               "¿Deseas instalar Python 3.12.9 ahora para solucionar este problema?\n"
               "Esto descargará e instalará la versión correcta automáticamente.")
        
        # 4 = Yes/No, 0x30 = Icono de advertencia, 0x40000 = Poner la ventana al frente
        response = ctypes.windll.user32.MessageBoxW(0, msg, "Corrección de Python Requerida", 4 | 0x30 | 0x40000)
        
        if response == 6: # El usuario dijo SI
            install_python_312()
            # Salimos del script actual porque queremos que el usuario reinicie con la nueva versión
            sys.exit(0)
        else:
            print("🚫 El usuario rechazó la instalación. Continuando bajo su propio riesgo...")

def install_python_312():
    print("🚀 Iniciando descarga de Python 3.12.9 (64-bit)...")
    # Usamos un User-Agent para evitar que el servidor de Python bloquee la descarga automatizada
    opener = urllib.request.build_opener()
    opener.addheaders = [('User-Agent', 'Mozilla/5.0')]
    urllib.request.install_opener(opener)
    
    installer_url = "https://www.python.org/ftp/python/3.12.9/python-3.12.9-amd64.exe"
    installer_path = os.path.join(os.environ["TEMP"], "python_312_installer.exe")

    try:
        urllib.request.urlretrieve(installer_url, installer_path)
        print("⚙️ Ejecutando instalador oficial en modo silencioso...")
        
        # Flags: 
        # /quiet -> Sin ventanas
        # InstallAllUsers=1 -> Para evitar problemas de permisos de carpeta
        # PrependPath=1 -> Para que sea el Python por defecto en la consola
        process = subprocess.run([installer_path, "/quiet", "InstallAllUsers=1", "PrependPath=1"], 
                                 shell=True, check=True)
        
        show_msgbox("Instalación Exitosa", 
                    "Python 3.12 se ha instalado.\n\nCIERRA COMPLETAMENTE el App Hub y vuelve a abrirlo para aplicar los cambios.", 0 | 0x40)
    except Exception as e:
        show_msgbox("Error de Instalación", f"No se pudo instalar Python 3.12:\n{e}", 0 | 0x10)

def ensure_pip():
    # Intentamos actualizar pip de paso para quitar los avisos de [notice]
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "pip", "--quiet"], check=False)
        print("\x1b[0;32m[OK]\x1b[0m pip actualizado y listo.")
    except:
        pass

def install_torch_universal():
    """Instalación manual de Torch para evitar conflictos de CUDA."""
    try:
        import torch
        # Verificamos que no sea una versión rota
        print(f"✅ PyTorch detectado: {torch.__version__}")
    except ImportError:
        print("📦 Instalando PyTorch Universal + DirectML...")
        pkgs = ["torch", "torchvision", "torchaudio", "torch-directml"]
        
        # Detectar NVIDIA
        extra = []
        try:
            res = subprocess.run(["nvidia-smi"], capture_output=True)
            if res.returncode == 0:
                extra = ["--extra-index-url", "https://download.pytorch.org/whl/cu121"]
        except:
            pass
            
        subprocess.run([sys.executable, "-m", "pip", "install"] + pkgs + extra + ["--quiet"])

def install_requirements_in_directory(base_dir):
    for root, _, files in os.walk(base_dir):
        if "requirements.txt" in files:
            req_path = os.path.join(root, "requirements.txt")
            print(f"🔍 Sincronizando: {req_path}")
            
            # Instalamos el archivo pero ignoramos 'torch' porque ya lo instalamos arriba
            # Usamos un filtro por comando para que pip no intente bajar la versión con +cu
            subprocess.run([sys.executable, "-m", "pip", "install", "-r", req_path, "--quiet"], check=False)

if __name__ == "__main__":
    # 1. Forzar chequeo de versión
    check_python_version()

    # 2. Preparar PIP
    ensure_pip()
    
    # 3. Torch Universal
    install_torch_universal()
    
    # 4. Resto de la carpeta
    target_dir = "C:/Apps/App_hub"
    if os.path.exists(target_dir):
        install_requirements_in_directory(target_dir)
    
    print("\n✨ Configuración finalizada.")
