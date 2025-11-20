import os
from download import download_file
import boto3

# REPO_PATH = "./SentinelOne-agent"
DOWNLOAD_DIR = "/tmp/downloads"         # Directory to save the downloaded files


def lambda_handler(event, context):
    """
    The main function that orchestrates the downloading of packages, creating a GitHub release,
    and uploading the downloaded assets to the release.
    """

    """Lambda entry point."""
    WINDOWS_GROUP_ONE_URL = "https://usea1-001-mssp.sentinelone.net/web/api/v2.1/update/agent/packages?fileExtension=.msi&limit=1&osArches=64%20bit&osTypes=windows&skip=1&sortBy=version&sortOrder=desc&status=ga"
    WINDOWS_GROUP_TWO_URL_X32 = "https://usea1-001-mssp.sentinelone.net/web/api/v2.1/update/agent/packages?fileExtension=.msi&majorVersions=23.4&osArches=32%20bit&osTypes=windows&sortBy=version&sortOrder=desc&status=ga&limit=1"
    WINDOWS_GROUP_TWO_URL_X64 = "https://usea1-001-mssp.sentinelone.net/web/api/v2.1/update/agent/packages?fileExtension=.msi&majorVersions=23.4&osArches=64%20bit&osTypes=windows&sortBy=version&sortOrder=desc&status=ga&limit=1"
    MAC_GROUP_URL = "https://usea1-001-mssp.sentinelone.net/web/api/v2.1/update/agent/packages?osTypes=macos&sortBy=version&sortOrder=desc&status=ga"

    """NEW LINKS REQUESTED BY MITS"""
    WINDOWS_GROUP_ONE_X86_URL = "https://usea1-001-mssp.sentinelone.net/web/api/v2.1/update/agent/packages?fileExtension=.msi&limit=1&osArches=64%20bit&osTypes=windows&skip=1&sortBy=version&sortOrder=desc&status=ga"
    WINDOWS_GROUP_ONE_ARM_URL = "https://usea1-001-mssp.sentinelone.net/web/api/v2.1/update/agent/packages?limit=1&osArches=ARM64&platformType=windows&skip=1&sortBy=version&sortOrder=desc&status=ga"

    WINDOWS_GROUP_ONE_NAME = "SentinelInstaller_windows_64bit_MSI_Latest_Group1.msi"
    WINDOWS_GROUP_TWO_NAME_X32 = "SentinelInstaller_windows_32bit_MSI_Latest_Group2.msi"
    WINDOWS_GROUP_TWO_NAME_X64 = "SentinelInstaller_windows_64bit_MSI_Latest_Group2.msi"
    MAC_GROUP_NAME = "SentinelInstaller_macos_Latest.pkg"

    """NAME FOR THE NEW URLS"""
    WINDOWS_GROUP_ONE_X64_NAME = "SentinelInstaller_windows_x64_Latest.msi"
    WINDOWS_GROUP_ONE_ARM_NAME = "SentinelInstaller_windows_ARM_Latest.exe"

    print("I\'m running")

    try:
        windows_group_one_file = os.path.join(
            DOWNLOAD_DIR, WINDOWS_GROUP_ONE_NAME)
        download_file(WINDOWS_GROUP_ONE_URL, windows_group_one_file)
        
        windows_group_two_file = os.path.join(
            DOWNLOAD_DIR, WINDOWS_GROUP_TWO_NAME_X32)
        download_file(WINDOWS_GROUP_ONE_URL_X32, windows_group_two_file_32)
        
        windows_group_two_file = os.path.join(
            DOWNLOAD_DIR, WINDOWS_GROUP_TWO_NAME_X64)
        download_file(WINDOWS_GROUP_TWO_URL_X64, windows_group_two_file_64)
        
        mac_group_file = os.path.join(DOWNLOAD_DIR, MAC_GROUP_NAME)
        download_file(MAC_GROUP_URL, mac_group_file)

        # AWS S3 Instead
        # Bucket Name: s1-rsmd-installers, key s1/ + filename
        # https://boto3.amazonaws.com/v1/documentation/api/latest/guide/s3-uploading-files.html
        s3 = boto3.resource('s3')
        s3_client = boto3.client('s3')
        s3_client.upload_file(Filename=windows_group_one_file,
                              Key=f"s1/{WINDOWS_GROUP_ONE_NAME}", Bucket="s1-rsmd-installers")
        s3_client.upload_file(Filename=windows_group_two_file_32,
                              Key=f"s1/{WINDOWS_GROUP_TWO_NAME_X32}", Bucket="s1-rsmd-installers")
         s3_client.upload_file(Filename=windows_group_two_file_64,
                              Key=f"s1/{WINDOWS_GROUP_TWO_NAME_X64}", Bucket="s1-rsmd-installers")
        s3_client.upload_file(
            Filename=mac_group_file, Key=f"s1/{MAC_GROUP_NAME}", Bucket="s1-rsmd-installers")

        """FILE FOR THE NEW URLS"""
        windows_group_one_X86_file = os.path.join(
            DOWNLOAD_DIR, WINDOWS_GROUP_ONE_X64_NAME)
        download_file(WINDOWS_GROUP_ONE_X64_URL, windows_group_one_X64_file)
        windows_group_one_ARM_file = os.path.join(
            DOWNLOAD_DIR, WINDOWS_GROUP_ONE_ARM_NAME)
        download_file(WINDOWS_GROUP_ONE_ARM_URL, windows_group_one_ARM_file)

        """UPLOAD THE NEW AGENTS FILES"""
        s3_client.upload_file(
            Filename=windows_group_one_X64_file, Key=f"s1/{WINDOWS_GROUP_ONE_X64_NAME}", Bucket="s1-rsmd-installers")
        s3_client.upload_file(
            Filename=windows_group_one_ARM_file, Key=f"s1/{WINDOWS_GROUP_ONE_ARM_NAME}", Bucket="s1-rsmd-installers")

        return {"status": "Success"}
    except Exception as e:
        print(f"Error: {e}")
        return {"status": "Failed", "error": str(e)}
