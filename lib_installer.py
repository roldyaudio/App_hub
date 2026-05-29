import os
import subprocess
import sys
from pathlib import Path

APP_DIR = Path(__file__).resolve().parent

def ensure_pip():
    try:
        subprocess.run([sys.executable, "-m", "pip", "--version"],
                       check=True, capture_output=True)
        print("\x1b[0;32m[OK]\x1b[0m pip is ready.")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("pip not found. Installing...")
        subprocess.check_call([sys.executable, "-m", "ensurepip"])

def install_requirements_in_directory(base_dir):
    """
    Scans the directory for requirements.txt and installs them.
    Note: Manual 'setuptools' upgrade was removed to prevent version conflicts
    with specific constraints in the requirements.txt file.
    """
    base_dir = Path(base_dir)
    for root, dirs, files in os.walk(base_dir):
        for file in files:
            if file == "requirements.txt":
                req_path = Path(root) / file
                print(f"\n🚀 Checking dependencies: {req_path}")

                # Using --quiet to avoid spamming the console if requirements are already met.
                # pip will only perform actions if the current version doesn't match the .txt file.
                result = subprocess.run(
                    [sys.executable, "-m", "pip", "install", "-r", str(req_path), "--quiet"]
                )

                if result.returncode == 0:
                    print(f"✅ Environment is synchronized.")
                else:
                    print(f"❌ Error installing from {req_path}")
                    sys.exit(1)

if __name__ == "__main__":
    # Ensure environment is ready
    ensure_pip()

    # Process the launcher directory instead of relying on the shell's working directory.
    install_requirements_in_directory(APP_DIR)

    print("\n✨ Process completed successfully.")
