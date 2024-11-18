import os
import requests
from typing import List

# Configuration Constants
REPO_OWNER = "RSM-DEFENSE-ENGINEERING"  # GitHub org
REPO_NAME = "packages-test"              # Replace with your repository name
TOKEN = ""
TAG_NAME = "v1.0.0"                  # The tag for the release
RELEASE_NAME = f"Release {TAG_NAME}"  # Name of the release
BODY = f"Automated release for {TAG_NAME}."  # Release description
ARCH_TYPES: List[str] = ["arm", "32", "64"]  # Supported architecture types
# Supported operating systems
OS_TYPES: List[str] = ["linux", "windows", "mac"]
DOWNLOAD_DIR = "./downloads"         # Directory to save the downloaded files
# Vendor API endpoint for latest release
VENDOR_API_URL = "https://usea1-001-mssp.sentinelone.net/web/api/v2.1/update/agent/packages"

# GitHub API URL
GITHUB_API_URL = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}"

# Ensure the download directory exists
os.makedirs(DOWNLOAD_DIR, exist_ok=True)


def download_file(url: str, dest: str) -> None:
    """
    Downloads a file from the provided URL and saves it to the destination.

    Args:
        url (str): The URL from which to download the file.
        dest (str): The destination path to save the downloaded file.

    Raises:
        requests.exceptions.RequestException: If the download fails.
    """
    print(f"Downloading: {url}")
    response = requests.get(url, stream=True)
    response.raise_for_status()  # Will raise an exception for HTTP errors

    with open(dest, "wb") as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)

    print(f"Downloaded: {dest}")


def create_github_release() -> int:
    """
    Creates a new GitHub release using the GitHub API.

    Returns:
        int: The ID of the created GitHub release.

    Raises:
        requests.exceptions.RequestException: If the release creation fails.
    """
    headers = {"Authorization": f"token {TOKEN}"}
    data = {
        "tag_name": TAG_NAME,
        "name": RELEASE_NAME,
        "body": BODY,
        "draft": False,
        "prerelease": False,
    }

    response = requests.post(
        f"{GITHUB_API_URL}/releases", json=data, headers=headers)
    response.raise_for_status()  # Will raise an exception if the API call fails

    release = response.json()
    print(f"GitHub release created: {release['html_url']}")
    return release["id"]


def upload_asset(release_id: int, file_path: str) -> None:
    """
    Uploads an asset (file) to a specific GitHub release.

    Args:
        release_id (int): The ID of the GitHub release to upload to.
        file_path (str): The file path of the asset to upload.

    Raises:
        requests.exceptions.RequestException: If the asset upload fails.
    """
    headers = {"Authorization": f"token {TOKEN}"}
    file_name = os.path.basename(file_path)

    with open(file_path, "rb") as f:
        response = requests.post(
            f"{GITHUB_API_URL}/releases/{release_id}/assets?name={file_name}",
            headers=headers,
            data=f,
            params={"name": file_name},
        )

    response.raise_for_status()  # Will raise an exception if the API call fails
    print(f"Uploaded: {file_name}")


def main() -> None:
    """
    The main function that orchestrates the downloading of packages, creating a GitHub release,
    and uploading the downloaded assets to the release.
    """
    # Step 1: Download the packages from the vendor API
    for os_type in OS_TYPES:
        for arch in ARCH_TYPES:
            package_name = f"package-{os_type}-{arch}.tar.gz"
            download_url = f"{VENDOR_API_URL}?os={os_type}&arch={arch}"

            # Download the file to the specified directory
            download_file(download_url, os.path.join(
                DOWNLOAD_DIR, package_name))

    # Step 2: Create the GitHub release
    release_id = create_github_release()

    # Step 3: Upload the downloaded files to GitHub release
    for file in os.listdir(DOWNLOAD_DIR):
        file_path = os.path.join(DOWNLOAD_DIR, file)
        upload_asset(release_id, file_path)


if __name__ == "__main__":
    main()
