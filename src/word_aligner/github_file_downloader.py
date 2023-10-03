from github import Github

from .github_token import GITHUB_TOKEN

TOKEN = GITHUB_TOKEN
REPO_OWNER = "MonlamAI"


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
                return None

        except Exception as error:
            print(f"An error occurred: {error}")
            return None


if __name__ == "__main__":
    # Usage example
    tm_file_name = "TM079"
    downloader = GitHubFileDownloader(TOKEN, REPO_OWNER, tm_file_name)
    bo_url, en_url = downloader.get_download_urls_from_repo()
    print(bo_url)
    print(en_url)
