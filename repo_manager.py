import subprocess
import json
import os
import threading
import sys

# JSON FUNCTIONS
def load_repos():
    with open('repos.json', 'r') as file:
        data = json.load(file)
        return data["download_path"], data["repos"]


def clone_or_update_repo(repo_url, download_path, file_to_run):
    try:
        repo_name = repo_url.split('/')[-1].replace('.git', '')
        repo_path = os.path.join(download_path, repo_name)

        if os.path.exists(repo_path):
            # Pull updates if the repository exists
            result = subprocess.run(["git", "-C", repo_path, "pull"], capture_output=True, text=True)
            if result.returncode == 0:
                print(f"✅ Repository {repo_url} updated successfully.")
                # run_file(repo_path, file_to_run)
            else:
                print(f"❌ Error updating repository: {result.stderr}")
        else:
            # Clone the repository if it doesn't exist
            result = subprocess.run(["git", "clone", repo_url, repo_path], capture_output=True, text=True)
            if result.returncode == 0:
                print(f"✅ Repository {repo_url} cloned successfully to {repo_path}.")
                run_file(repo_path, file_to_run)
            else:
                print(f"❌ Error cloning repository: {result.stderr}")
    except Exception as e:
        print(f"⚠ An unexpected error occurred: {e}")


def clone_or_update_repo_async(repo_url, download_path, file_to_run):
    threading.Thread(target=clone_or_update_repo, args=(repo_url, download_path, file_to_run)).start()


def run_file(repo_path, file_to_run):
    if not file_to_run:
        return
    full_path = os.path.join(repo_path, file_to_run)
    if os.path.exists(full_path):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        # Verificar si es el mismo directorio donde se ejecuta el hub
        if os.path.samefile(repo_path, current_dir):
            print(f"🔄 Repo is the hub itself. Restarting with updated code: {full_path}")
            os.execv(sys.executable, ['python', full_path])
        else:
            print(f"🚀 Launching external app: {full_path}")
            subprocess.Popen(['python', full_path])
    else:
        print(f"⚠ File {full_path} does not exist.")
