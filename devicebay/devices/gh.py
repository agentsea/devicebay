from typing import Optional, List, Dict

from pydantic import BaseModel

from github import Github, PullRequest, Issue
from github.Issue import Issue
from github.Repository import Repository
from github.PullRequest import PullRequest

from devicebay import Device, action, observation


class GitHubConnectConfig(BaseModel):
    """Connect configuration for GitHub"""

    access_token: str


class GitHubProvisionConfig(BaseModel):
    """Provision configuration for GitHub"""

    repo: str


class GitHub(Device[GitHubConnectConfig, "GitHub", GitHubProvisionConfig]):
    """A GitHub device"""

    def __init__(self, config: GitHubConnectConfig) -> None:
        super().__init__()
        self._config = config
        self._github = Github(config.access_token)

    @observation
    def get_repository(self, name: str) -> Repository:
        """Get a repository by name

        Args:
            name (str): Name of the repository

        Returns:
            Repository: The repository
        """
        return self._github.get_user().get_repo(name)

    @action
    def create_pull_request(
        self, repo_name: str, title: str, head: str, base: str, body: str = ""
    ) -> None:
        """Create a pull request

        Args:
            repo_name (str): Name of the repository
            title (str): Title of the pull request
            head (str): Branch name or commit SHA of the head
            base (str): Branch name of the base
            body (str, optional): Body of the pull request. Defaults to "".
        """
        repo: Repository = self.get_repository(repo_name)
        repo.create_pull(title=title, body=body, head=head, base=base)

    @observation
    def get_pull_request(self, repo_name: str, pr_number: int) -> PullRequest:
        """Get a pull request by number

        Args:
            repo_name (str): Name of the repository
            pr_number (int): Number of the pull request

        Returns:
            PullRequest: The pull request
        """
        repo: Repository = self.get_repository(repo_name)
        return repo.get_pull(pr_number)

    @action
    def comment_on_pull_request(
        self, repo_name: str, pr_number: int, body: str
    ) -> None:
        """Comment on a pull request

        Args:
            repo_name (str): Name of the repository
            pr_number (int): Number of the pull request
            body (str): Body of the comment
        """
        pr: PullRequest = self.get_pull_request(repo_name, pr_number)
        pr.create_issue_comment(body)

    @action
    def create_issue(
        self,
        repo_name: str,
        title: str,
        body: str = "",
        assignee: Optional[str] = None,
        labels: Optional[List[str]] = None,
    ) -> None:
        """Create an issue

        Args:
            repo_name (str): Name of the repository
            title (str): Title of the issue
            body (str, optional): Body of the issue. Defaults to "".
            assignee (str, optional): Username of the assignee. Defaults to None.
            labels (List[str], optional): List of label names. Defaults to None.
        """
        repo: Repository = self.get_repository(repo_name)
        repo.create_issue(title=title, body=body, assignee=assignee, labels=labels)  # type: ignore

    @observation
    def get_issue(self, repo_name: str, issue_number: int) -> Issue:
        """Get an issue by number

        Args:
            repo_name (str): Name of the repository
            issue_number (int): Number of the issue

        Returns:
            Issue: The issue
        """
        repo: Repository = self.get_repository(repo_name)
        return repo.get_issue(issue_number)

    @action
    def comment_on_issue(self, repo_name: str, issue_number: int, body: str) -> None:
        """Comment on an issue

        Args:
            repo_name (str): Name of the repository
            issue_number (int): Number of the issue
            body (str): Body of the comment
        """
        issue: Issue = self.get_issue(repo_name, issue_number)
        issue.create_comment(body)

    def _get_repository_contents_recursive(
        self, repo: Repository, path: str
    ) -> List[Dict[str, str]]:
        """Recursively get the contents of a repository

        Args:
            repo (Repository): The repository
            path (str): Path of the directory

        Returns:
            List[Dict[str, str]]: List of file information
        """
        contents = repo.get_contents(path)
        if not isinstance(contents, list):
            contents = [contents]

        files = []
        for content in contents:
            if content.type == "dir":
                files.extend(
                    self._get_repository_contents_recursive(repo, content.path)
                )
            else:
                files.append(
                    {"path": content.path, "name": content.name, "type": content.type}
                )
        return files

    @observation
    def list_repository_files(self, repo_name: str) -> List[Dict[str, str]]:
        """List all files in a repository

        Args:
            repo_name (str): Name of the repository

        Returns:
            List[Dict[str, str]]: List of file information
        """
        repo: Repository = self.get_repository(repo_name)
        return self._get_repository_contents_recursive(repo, "")

    @observation
    def get_repository_files(self, repo_name: str) -> Dict[str, str]:
        """Get all files in a repository

        Args:
            repo_name (str): Name of the repository

        Returns:
            Dict[str, str]: Dictionary of file paths and their contents
        """
        repo: Repository = self.get_repository(repo_name)
        files = self._get_repository_contents_recursive(repo, "")
        file_contents = {}
        for file in files:
            content = repo.get_contents(file["path"])
            if isinstance(content, list):
                continue  # Skip directories
            file_contents[file["path"]] = content.decoded_content.decode("utf-8")
        return file_contents

    @observation
    def get_repository_file(self, repo_name: str, path: str) -> str:
        """Get a single file from a repository

        Args:
            repo_name (str): Name of the repository
            path (str): Path of the file

        Returns:
            str: Content of the file
        """
        repo: Repository = self.get_repository(repo_name)
        content = repo.get_contents(path)
        if isinstance(content, list):
            raise ValueError(f"Path '{path}' points to a directory, not a file.")
        return content.decoded_content.decode("utf-8")
