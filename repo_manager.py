import subprocess
import json

# JSON FUNCTIONS
def load_repos():
    with open('repos.json', 'r') as file:
        data = json.load(file)
        return data["download_path"], data["repos"]


def clone_repo(repo_url, download_path):
    try:
        # Clonar en la ruta especificada
        result = subprocess.run(["git", "clone", repo_url, download_path], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"Repository {repo_url} cloned successfully to {download_path}.")
        else:
            print(f"Error cloning repository: {result.stderr}")
    except Exception as e:
        print(f"An unexpected error occurred while cloning: {e}")