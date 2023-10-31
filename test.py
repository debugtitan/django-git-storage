import unittest
from unittest.mock import MagicMock, patch
from git_storage.storage import GithubStorage

class TestGithubStorage(unittest.TestCase):

    def setUp(self):
        self.github_mock = MagicMock()
        self.storage = GithubStorage()

    @patch('git_storage.storage.Github')
    def test_get_authenticated_github_user(self, github_mock):
        github_mock.return_value.get_user.return_value.login = "testuser"
        authenticated_user = self.storage.get_authenticated_github_user().get_user()
        self.assertEqual(authenticated_user.login, "testuser")
        
        github_mock.side_effect = Exception("Invalid token")
        with self.assertRaises(Exception):
            self.storage.get_authenticated_github_user()

if __name__ == '__main__':
    unittest.main()

