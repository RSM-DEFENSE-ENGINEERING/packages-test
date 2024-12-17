from git import Repo
import shutil
import os

# Configure your paths and messages
commit_message = "Automated commit: Added new files from FTP server"
REMOTE = "git@github.com:RSM-DEFENSE-ENGINEERING/SentinelOne-agent.git"

# Open the repository


def pull_latest(repo: Repo):
    """Pull the latest changes from the remote repository."""
    origin = repo.remotes.origin
    origin.pull()
    print("Pulled the latest changes.")


def copy_new_files(source_folder: str, repo_path: str):
    """Copy new files from the source folder to the Git repository."""
    for item in os.listdir(source_folder):
        source_path = os.path.join(source_folder, item)
        dest_path = os.path.join(repo_path, item)

        if os.path.isdir(source_path):
            shutil.copytree(source_path, dest_path, dirs_exist_ok=True)
        else:
            shutil.copy2(source_path, dest_path)

    print(f"Copied files from {source_folder} to {repo_path}.")


def stage_and_commit(repo: Repo):
    """Stage changes and commit them to the repository."""
    repo.git.add(A=True)  # Stage all changes
    if repo.is_dirty():
        repo.index.commit(commit_message)
        print("Committed changes.")
    else:
        print("No changes to commit.")


def push_changes(repo: Repo):
    """Push the committed changes to the remote repository."""
    origin = repo.remotes.origin
    origin.push()
    print("Pushed changes to the remote repository.")


def get_repo(repo_path: str) -> Repo:
    repo = Repo(repo_path)
    return repo
