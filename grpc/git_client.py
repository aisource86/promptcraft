import os
import git
import json
from dotenv import load_dotenv

load_dotenv()

# GitHub credentials
GITHUB_USERNAME = "hima707ch"
GITHUB_TOKEN = os.getenv("GITHUB_KEY")  # Generate from GitHub Developer Settings
REPO_NAME = "frontend-preview"  # Your repository name
BRANCH_NAME = "main"  # Specify the branch name
REPO_URL = f"https://{GITHUB_USERNAME}:{GITHUB_TOKEN}@github.com/{GITHUB_USERNAME}/{REPO_NAME}.git"
LOCAL_REPO_PATH = "./temp_repo-2"

def push_client_code(json_response, sub_folder = "", push=False):
    # Clone or initialize repo
    if os.path.exists(LOCAL_REPO_PATH):
        repo = git.Repo(LOCAL_REPO_PATH)
        # repo.git.pull("origin", BRANCH_NAME)  # Pull latest changes from specific branch
    else:
        repo = git.Repo.clone_from(REPO_URL, LOCAL_REPO_PATH, branch=BRANCH_NAME)

    # Create components folder inside src if not exists
    src_folder = os.path.join(LOCAL_REPO_PATH, "src")
    components_folder = os.path.join(src_folder, "components", sub_folder)
    os.makedirs(components_folder, exist_ok=True)

    # Write all files (Git will ignore unchanged ones)
    for filename, content in json_response.items():
        file_path = os.path.join(components_folder, filename)
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(content)

    # Commit and push only if there are changes
    if repo.is_dirty(untracked_files=True):
        repo.git.add(A=True)
        repo.index.commit("Updated React components from JSON")

        # Ensure we are on the correct branch
        if repo.active_branch.name != BRANCH_NAME:
            repo.git.checkout(BRANCH_NAME)  

        if push:
            # Push to the specific branch
            origin = repo.remote(name="origin")
            origin.push(refspec=f"{BRANCH_NAME}:{BRANCH_NAME}")
            print(f"🚀 Changes pushed to GitHub branch '{BRANCH_NAME}' successfully!")
        else:
            print("!!Changes Commited")
    else:
        if push:
            # Push to the specific branch
            origin = repo.remote(name="origin")
            origin.push(refspec=f"{BRANCH_NAME}:{BRANCH_NAME}")
            print(f"🚀 Changes pushed to GitHub branch '{BRANCH_NAME}' successfully!")
        else:
            print("✅ No changes detected. Nothing to push.")

