import os
import git
import json
from dotenv import load_dotenv

load_dotenv()


# GitHub credentials
GITHUB_USERNAME = "hima707ch"
GITHUB_TOKEN = os.getenv("GITHUB_KEY")  # Generate from GitHub Developer Settings
REPO_NAME = "backend-preview"  # Your repository name
REPO_URL = f"https://{GITHUB_USERNAME}:{GITHUB_TOKEN}@github.com/{GITHUB_USERNAME}/{REPO_NAME}.git"
LOCAL_REPO_PATH = "./temp_backend"

def push_server_code(json_response):
    if os.path.exists(LOCAL_REPO_PATH):
        repo = git.Repo(LOCAL_REPO_PATH)
        repo.git.pull()  # Pull latest changes
    else:
        repo = git.Repo.clone_from(REPO_URL, LOCAL_REPO_PATH)

    root_folder = os.path.join(LOCAL_REPO_PATH, "")
    os.makedirs(root_folder, exist_ok=True)

    for filename, content in json_response.items():

        file_path = os.path.join(root_folder, filename)
        file_dir = os.path.dirname(file_path)  
        
        if file_dir:
            os.makedirs(file_dir, exist_ok=True)

        # Write content to the file
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(content)
    
    # Commit and push only if there are changes
    if repo.is_dirty(untracked_files=True):  
        repo.git.add(A=True)
        repo.index.commit("Updated Backend code from server")
        origin = repo.remote(name="origin")
        origin.push()
        print("🚀 Changes pushed to GitHub successfully!")
    else:
        print("✅ No changes detected. Nothing to push.")
