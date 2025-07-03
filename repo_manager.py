import subprocess
import json
import os
import threading

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
                print(f"Repository {repo_url} updated successfully.")
            else:
                print(f"Error updating repository: {result.stderr}")
            run_file(repo_path, file_to_run)  # Run the file after updating
        else:
            # Clone the repository if it doesn't exist
            result = subprocess.run(["git", "clone", repo_url, repo_path], capture_output=True, text=True)
            if result.returncode == 0:
                print(f"Repository {repo_url} cloned successfully to {repo_path}.")
                run_file(repo_path, file_to_run)  # Optionally run the file after cloning
            else:
                print(f"Error cloning repository: {result.stderr}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def clone_or_update_repo_async(repo_url, download_path, file_to_run):
    threading.Thread(target=clone_or_update_repo, args=(repo_url, download_path, file_to_run)).start()

def run_file(repo_path, file_to_run):
    full_path = os.path.join(repo_path, file_to_run)
    if os.path.exists(full_path):
        subprocess.run(["python", full_path], check=True)
    else:
        print(f"File {full_path} does not exist.")