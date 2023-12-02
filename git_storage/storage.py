import requests
import secrets

from django.core.files import storage
from django.core.files.base import ContentFile
from django.core.files.uploadedfile import UploadedFile

from github import Github, Auth, BadCredentialsException, UnknownObjectException

from .base import GIT_STORAGE_CONFIG as GIT_STORAGE


class GithubStorage(storage.Storage):
    token, storage_repo = GIT_STORAGE["GIT_ACCESS_TOKEN"], GIT_STORAGE["GIT_REPO"]
    def __init__(self) -> None:
        self.user = self.get_authenticated_github_user()
        self.repo = self.fetch_storage_repo()

    def get_available_name(self, name, max_length=4) -> str:
        return str(secrets.token_hex(max_length)) + name

    def get_authenticated_github_user(self):
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
                return auth
        except BadCredentialsException as e:
            raise BadCredentialsException(
                400, message="Invalid github access token"
            ) from e

    def fetch_storage_repo(self):
        """
        The function fetches a storage repository from a user's repository using the user and repo
        attributes.
        :return: The code is returning the storage repository associated with the user and repository
        specified.
        """
        try:
            return self.user.get_repo(self.storage_repo)
        except UnknownObjectException:
            raise UnknownObjectException(
                400, message=f"Storage repository `{self.storage_repo}` not found"
            )

    def _open(self, name, mode="rb"):
        """
        The function opens a file from a given URL and returns it as a ContentFile object.

        :param name: The `name` parameter is the name or path of the file that you want to open. It is
        used to construct the URL for the file and set the name of the `ContentFile` object
        :param mode: The 'mode' parameter specifies the mode in which the file should be opened. It is
        an optional parameter with a default value of 'rb', which stands for "read binary". This mode is
        used for reading binary files, such as images or videos. Other possible values for the 'mode'
        parameter, defaults to rb (optional)
        :return: a file object.
        """
        url = self._get_url(name)
        response = requests.get(url)
        if response.status_code == 404:
            raise IOError
        response.raise_for_status()
        file = ContentFile(response.content)
        file.name = name
        file.mode = mode
        return file

    def _upload(self, name, content):
        """
        The `_upload` function creates a file in a repository and returns the contents of the file.

        :param name: The name of the file to be uploaded
        :param content: The `content` parameter is expected to be a file-like object that contains the
        content to be uploaded. It should support the `read()` method, which will be used to read the
        content of the file
        :return: The method `_upload` returns the contents of the file that was uploaded.
        """
        # try:
        name = self.get_available_name(name)
        self.repo.create_file(name, f"git-storage {name}", content.read())
        # except Exception as e:
        # print(e)
        return self.repo.get_contents(name)

    def save(self, name, content, max_length=None):
        """
        The function saves an uploaded file with a given name and content, and returns the name of the
        saved file.

        :param name: The name parameter is the name of the file that you want to save. It is a string
        that represents the name of the file
        :param content: The content parameter is the file content that you want to save. It can be a
        file-like object or a string representing the file content
        :param max_length: The `max_length` parameter is an optional parameter that specifies the
        maximum length of the file name. If the file name exceeds this length, it will be truncated to
        fit within the specified limit. If `max_length` is not provided, there will be no limit on the
        length of the file name
        :return: The name of the uploaded file is being returned.
        """
        content = UploadedFile(content, name)
        response = self._upload(name, content)
        return response.name

    def _get_url(self, name):
        """
        The function `_get_url` takes a name parameter and returns the download URL of a file with that
        name in a GitHub repository.

        :param name: The `name` parameter is a string that represents the name of a file or directory in
        a GitHub repository
        :return: The download URL of the specified file on GitHub.
        """
        return self.repo.get_contents(name)

    def url(self, name):
        """
        The function returns the URL of a Github repository based on the given name.

        :param name: The `name` parameter is a string that represents the name of a Github repository
        :return: The method is returning the URL of a Github repository.
        """
        return self._get_url(name).download_url

    def exists(self, name):
        """
        The function checks if a resource exists by sending a HEAD request to its URL and returns True
        if the response status code is not 404.

        :param name: The `name` parameter is a string that represents the name of the resource you want
        to check for existence
        :return: a boolean value. If the response status code is 404, it returns False. Otherwise, it
        raises an exception if there is an error and returns True.
        """
        url = self._get_url(name)
        response = requests.head(url)
        if response.status_code == 404:
            return False
        response.raise_for_status()
        return True

    def delete(self, name):
        contents = self._get_url(name)
        response = self.repo.delete_file(
            contents.path, f"git-storage removed {name}", contents.sha
        )
        if response.status_code == 404:
            raise IOError(response.content)
        return 1

    def size(self, name):
        url = self._get_url(name)
        response = requests.head(url)
        if response.status_code == 200:
            return int(response.headers["content-length"])
        else:
            return None
