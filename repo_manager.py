import subprocess
import json
import os

# JSON FUNCTIONS
def load_repos():
    with open('repos.json', 'r') as file:
        data = json.load(file)
        return data["download_path"], data["repos"]


def clone_or_update_repo(repo_url, download_path):
    try:
        # Get the name of the repository from the URL
        repo_name = repo_url.split('/')[-1].replace('.git', '')
        repo_path = os.path.join(download_path, repo_name)

        if os.path.exists(repo_path):
            # If the repository already exists, update it
            result = subprocess.run(["git", "-C", repo_path, "pull"], capture_output=True, text=True)
            if result.returncode == 0:
                print(f"Repository {repo_url} updated successfully.")
            else:
                print(f"Error updating repository: {result.stderr}")
        else:
            # If the repository doesn't exist, clone it
            result = subprocess.run(["git", "clone", repo_url, repo_path], capture_output=True, text=True)
            if result.returncode == 0:
                print(f"Repository {repo_url} cloned successfully to {repo_path}.")
            else:
                print(f"Error cloning repository: {result.stderr}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
