from django.core.files import storage
from github import Github, Auth, BadCredentialsException,UnknownObjectException

from .base import Git_STORAGE

class GithubStorage(storage.Storage):
    token, repo  = Git_STORAGE["ACCESS_TOKEN"], Git_STORAGE["GIT_REPO"]
    def __init__(self) -> None:
        self.user = self.get_authenticated_github_user()
        self.repo = self.fetch_storage_repo()

    def get_authenticated_github_user(self) -> Github | None:
        """
        The function `get_authenticated_github_user` returns the authenticated GitHub user if the access
        token is valid.

        :return: an instance of the `Github` class if the authentication is successful and the user's
        login is valid. Otherwise, it returns `None`.
        """
        try:
            auth = Github(auth=Auth.Token(self.token))
            user = auth.get_user()
            if user.login:
                return user
        except BadCredentialsException as e:
            raise BadCredentialsException(400,message="Invalid github access token") from e


    def fetch_storage_repo(self):
        try:
            return self.user.get_repo(self.repo)
        except UnknownObjectException:
            raise UnknownObjectException(400,message="Storage repository not found")

