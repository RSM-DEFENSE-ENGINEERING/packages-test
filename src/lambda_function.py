from github import copy_new_files, pull_latest, stage_and_commit, push_changes, get_repo
from git import Repo
import os
from download import download_file
from ssh_agent import get_ssh_key, setup_ssh_agent

# REPO_PATH = "./SentinelOne-agent"
REPO_PATH = "git@github.com:RSM-DEFENSE-ENGINEERING/SentinelOne-agent.git"
DOWNLOAD_DIR = "/tmp/downloads"         # Directory to save the downloaded files


def commit_installers(repo: Repo):
    pull_latest(repo)
    copy_new_files(DOWNLOAD_DIR, REPO_PATH)
    stage_and_commit(repo)
    push_changes(repo)
    print("Git repository updated successfully!")


def lambda_handler(event, context):
    """
    The main function that orchestrates the downloading of packages, creating a GitHub release,
    and uploading the downloaded assets to the release.
    """

    """Lambda entry point."""
    WINDOWS_GROUP_ONE_URL = "https://usea1-001-mssp.sentinelone.net/web/api/v2.1/update/agent/packages?fileExtension=.msi&osArches=32 bit&osTypes=windows&sortBy=version&sortOrder=desc&status=ga"
    WINDOWS_GROUP_TWO_URL = "https://usea1-001-mssp.sentinelone.net/web/api/v2.1/update/agent/packages?fileExtension=.msi&majorVersions=23.4&osArches=32 bit&osTypes=windows&sortBy=version&sortOrder=desc&status=ga"
    MAC_GROUP_URL = "https://usea1-001-mssp.sentinelone.net/web/api/v2.1/update/agent/packages?osTypes=macos&sortBy=version&sortOrder=desc&status=ga"

    WINDOWS_GROUP_ONE_NAME = "SentinelInstaller_windows_32bit_MSI_Latest_Group1.zip"
    WINDOWS_GROUP_TWO_NAME = "SentinelInstaller_windows_32bit_MSI_Latest_Group2.zip"
    MAC_GROUP_NAME = "SentinelInstaller_macos_Latest.zip"
    print("I\'m running")

    try:
        download_file(WINDOWS_GROUP_ONE_URL, os.path.join(
            DOWNLOAD_DIR, WINDOWS_GROUP_ONE_NAME))

        download_file(WINDOWS_GROUP_TWO_URL, os.path.join(
            DOWNLOAD_DIR, WINDOWS_GROUP_TWO_NAME))
        download_file(MAC_GROUP_URL, os.path.join(
            DOWNLOAD_DIR, MAC_GROUP_NAME))

        ssh_key = get_ssh_key()
        setup_ssh_agent(ssh_key)
        print("SSH KEY RETRIEVED")
        repo = get_repo(REPO_PATH)
        commit_installers(repo)
        # Add your file copying logic here if needed
        return {"status": "Success"}
    except Exception as e:
        print(f"Error: {e}")
        return {"status": "Failed", "error": str(e)}


def main() -> None:
    lambda_handler({}, {})


if __name__ == "__main__":
    main()
