import os
import subprocess
import sys
import urllib.request
import ctypes # Para el cuadro de diálogo nativo de Windows

def show_msgbox(title, text, style):
    """Muestra un cuadro de diálogo de Windows (0: OK, 1: OK/Cancel, 4: Yes/No)"""
    return ctypes.windll.user32.MessageBoxW(0, text, title, style)

def check_python_version():
    """Verifica si la versión es 3.13+ y ofrece instalar 3.12 para compatibilidad con Audio."""
    if sys.version_info >= (3, 13):
        print("⚠️ Detectado Python 3.13+. Esta versión no es compatible con pydub (audioop).")
        
        msg = ("Se ha detectado Python 3.13. Las aplicaciones de audio requieren Python 3.12 para funcionar correctamente.\n\n"
               "¿Desea descargar e instalar Python 3.12 ahora?\n"
               "(Se instalará de forma oficial y se añadirá al PATH automáticamente)")
        
        # 4 = Yes/No button
        response = show_msgbox("Incompatibilidad de Audio Detectada", msg, 4)
        
        if response == 6: # 6 es "Yes"
            install_python_312()
        else:
            print("🚫 Instalación de Python 3.12 cancelada por el usuario. Es posible que el audio falle.")

def install_python_312():
    print("🚀 Iniciando descarga de Python 3.12.9...")
    installer_url = "https://www.python.org/ftp/python/3.12.9/python-3.12.9-amd64.exe"
    installer_path = os.path.join(os.environ["TEMP"], "python_312_installer.exe")

    try:
        urllib.request.urlretrieve(installer_url, installer_path)
        print("⚙️ Ejecutando instalador silencioso... Espere a que finalice.")
        # /quiet: sin ventanas, PrependPath: añade a variables de entorno
        subprocess.run([installer_path, "/quiet", "InstallAllUsers=1", "PrependPath=1"], check=True)
        
        show_msgbox("Instalación Completada", 
                    "Python 3.12 se ha instalado.\n\nPor favor, CIERRA el App Hub y vuelve a abrirlo para usar la versión correcta.", 0)
        sys.exit(0)
    except Exception as e:
        print(f"❌ Error instalando Python: {e}")

def ensure_pip():
    try:
        subprocess.run([sys.executable, "-m", "pip", "--version"], 
                       check=True, capture_output=True)
        print("\x1b[0;32m[OK]\x1b[0m pip is ready.")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("pip not found. Installing...")
        subprocess.check_call([sys.executable, "-m", "ensurepip"])

def install_torch_universal():
    """Instala PyTorch compatible con cualquier GPU o CPU."""
    # Verificamos si ya existe torch
    try:
        import torch
        print("\x1b[0;32m[OK]\x1b[0m PyTorch ya está presente.")
        return
    except ImportError:
        print("📦 Instalando motor de procesamiento universal (PyTorch + DirectML)...")
        
        # Paquetes base + soporte para AMD/Intel (DirectML)
        packages = ["torch", "torchvision", "torchaudio", "torch-directml"]
        
        # Detectar si hay NVIDIA para usar su servidor de alta velocidad
        extra_url = []
        try:
            subprocess.run(["nvidia-smi"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            extra_url = ["--extra-index-url", "https://download.pytorch.org/whl/cu121"]
        except:
            pass

        subprocess.run([sys.executable, "-m", "pip", "install"] + packages + extra_url + ["--quiet"])

def install_requirements_in_directory(base_dir):
    for root, dirs, files in os.walk(base_dir):
        for file in files:
            if file == "requirements.txt":
                req_path = os.path.join(root, file)
                print(f"\n🚀 Checking dependencies: {req_path}")
                
                # Leemos el archivo para saltar torch si ya lo manejamos nosotros
                try:
                    with open(req_path, 'r') as f:
                        lines = f.readlines()
                    
                    # Filtramos torch del requirements para que no cause error +cu121
                    filtered_reqs = [l.strip() for l in lines if "torch" not in l.lower()]
                    
                    for req in filtered_reqs:
                        if req:
                            subprocess.run([sys.executable, "-m", "pip", "install", req, "--quiet"])
                    
                    print(f"✅ Environment is synchronized.")
                except Exception as e:
                    print(f"❌ Error processing {req_path}: {e}")

if __name__ == "__main__":
    # 1. Comprobar versión de Python (Incompatibilidad 3.13)
    check_python_version()

    # 2. Asegurar pip
    ensure_pip()
    
    # 3. Instalación inteligente de Torch (Universal)
    install_torch_universal()
    
    # 4. Resto de librerías del Hub
    target_dir = "C:/Apps/App_hub"
    if os.path.exists(target_dir):
        install_requirements_in_directory(target_dir)
    
    print("\n✨ Process completed successfully.")
