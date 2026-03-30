import os
import subprocess
import sys

def ensure_pip():
    """Checks if pip is installed; if not, installs it using ensurepip."""
    try:
        import pip
        print("\x1b[0;32m[OK]\x1b[0m pip is already installed.")
    except ImportError:
        print("pip not found. Installing with ensurepip...")
        subprocess.check_call([sys.executable, "-m", "ensurepip"])

def install_requirements_in_directory(base_dir):
    """
    Scans the directory for requirements.txt and installs them.
    Note: Manual 'setuptools' upgrade was removed to prevent version conflicts 
    with specific constraints in the requirements.txt file.
    """
    for root, dirs, files in os.walk(base_dir):
        for file in files:
            if file == "requirements.txt":
                req_path = os.path.join(root, file)
                print(f"\n🚀 Checking dependencies: {req_path}")
                
                # Using --quiet to avoid spamming the console if requirements are already met.
                # pip will only perform actions if the current version doesn't match the .txt file.
                result = subprocess.run(
                    [sys.executable, "-m", "pip", "install", "-r", req_path, "--quiet"]
                )
                
                if result.returncode == 0:
                    print(f"✅ Environment is synchronized.")
                else:
                    print(f"❌ Error installing from {req_path}")
                    sys.exit(1)

if __name__ == "__main__":
    # Ensure environment is ready
    ensure_pip()
    
    # Process the specific directory
    # Note: Hardcoding absolute paths is fine, but os.getcwd() is more portable.
    target_dir = "C:/Apps/App_hub"
    install_requirements_in_directory(target_dir)
    
    print("\n✨ Process completed successfully.")
