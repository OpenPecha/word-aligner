from pathlib import Path
from typing import List

import requests
from github import Github
from retrying import retry

from .config import LOG_FOLDER_DIR, RESOURCE_FOLDER_DIR, TMs_4006
from .github_token import GITHUB_TOKEN

TOKEN = GITHUB_TOKEN
REPO_OWNER = "MonlamAI"

ERROR_LOG_FILE = "Failed_to_download_TMs.txt"


class GitHubFileDownloader:
    def __init__(self, token, repo_owner, repo_name):
        self.token = token
        self.repo_owner = repo_owner
        self.repo_name = repo_name

    def get_download_urls_from_repo(self):
        # returns download urls of file with suffix 'bo.txt' or 'en.txt' in given repo
        g = Github(self.token)

        try:
            repo = g.get_repo(f"{self.repo_owner}/{self.repo_name}")
            contents = repo.get_contents("")

            bo_file_suffix = "bo.txt"
            en_file_suffix = "en.txt"

            bo_file_name = ""
            en_file_name = ""

            for content_file in contents:
                if content_file.name.endswith(bo_file_suffix):
                    bo_file_name = content_file.name
                if content_file.name.endswith(en_file_suffix):
                    en_file_name = content_file.name

            if bo_file_name and en_file_name:
                bo_download_url = repo.get_contents(bo_file_name).download_url
                en_download_url = repo.get_contents(en_file_name).download_url
                return bo_download_url, en_download_url

            else:
                print(f"{self.repo_name}: Either bo or en file is not present.")
                return None, None

        except Exception as error:
            print(f"{self.repo_name} An error occurred: {error}")
            write_to_error_log(ERROR_LOG_FILE, self.repo_name)
            return None, None


@retry(
    stop_max_attempt_number=3,  # Maximum number of retries
    wait_fixed=2000,  # Delay between retries in milliseconds (2 seconds)
    retry_on_exception=lambda x: isinstance(x, requests.exceptions.RequestException),
)
def download_file_with_url(
    download_url, new_downloaded_file_name, destination_folder="."
):

    response = requests.get(download_url)

    new_downloaded_file_name = new_downloaded_file_name
    output_path = Path(destination_folder) / new_downloaded_file_name
    if response.status_code == 200:
        with open(output_path, "wb") as local_file:
            local_file.write(response.content)
        print(f"File {new_downloaded_file_name} downloaded and saved to {output_path}")
    else:
        print(
            f"File {new_downloaded_file_name} failed to download file. Status code: {response.status_code}"
        )
        write_to_error_log(ERROR_LOG_FILE, new_downloaded_file_name)


def write_to_error_log(error_log_file, filename):
    error_log_file_path = LOG_FOLDER_DIR / error_log_file
    with open(error_log_file_path, "a") as log_file:
        log_file.write(f"{filename}: Failed to download \n")


def download_tm_files(tm_file_names: List[str], output_path=TMs_4006):
    tm_files_count = len(tm_file_names)
    tm_files_counter = 1
    for tm_file_name in tm_file_names:
        print(
            f"[{tm_files_counter}/{tm_files_count}] Downloading files for {tm_file_name}"
        )
        tm_files_counter += 1
        # Downloading bo, en files
        downloader = GitHubFileDownloader(TOKEN, REPO_OWNER, tm_file_name)
        bo_url, en_url = downloader.get_download_urls_from_repo()
        if bo_url is not None and en_url is not None:
            download_file_with_url(bo_url, f"{tm_file_name}-bo.txt", output_path)
            download_file_with_url(en_url, f"{tm_file_name}-en.txt", output_path)


if __name__ == "__main__":
    # Usage example
    tm_names_content = Path(RESOURCE_FOLDER_DIR / "tm_list.txt").read_text(
        encoding="utf-8"
    )
    tm_file_names = tm_names_content.split("\n")
    # Removing empty strings
    tm_file_names = [tm_file_name for tm_file_name in tm_file_names if tm_file_name]
    download_tm_files(tm_file_names)
