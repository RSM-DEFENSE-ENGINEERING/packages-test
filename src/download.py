import os
import urllib3

http = urllib3.PoolManager()
# Configuration Constants
S1_TOKEN = os.environ['S1_API_TOKEN']
DOWNLOAD_DIR = "/tmp/downloads"         # Directory to save the downloaded files

# Vendor API endpoint for latest release
VENDOR_API_URL = "https://usea1-001-mssp.sentinelone.net/web/api/v2.1/update/agent/packages"

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
    headers = {
        "Authorization": "ApiToken " + S1_TOKEN
    }

    print(f"Downloading: {url}")
    print(headers['Authorization'])
    response = http.request('GET', url, headers=headers, preload_content=False)

    with open(dest, 'wb') as f:
        while True:
            chunk = response.read(8192)
            if not chunk:
                break
            f.write(chunk)

    response.release_conn()
    print(f"Downloaded: {dest}")
