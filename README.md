# django-git-storages

Django Github Storage is a Django package that facilitates integration with [Github](http://github.com/)
by implementing [Django Storage API](https://docs.djangoproject.com/en/1.11/howto/custom-file-storage/).
With several lines of configuration, you can start using Github for yourfiles.
It uses [PyGithub](https://github.com/PyGithub/PyGithub) package under the hood.



It is simple to contribute to implement:
## Table of content

- [Requirements](#requirements)
- [Installation](#installation)
- [Settings](#settings)

## Requirements

The package requires Python 3.4+ and Django 3+.

## Installation

To install the package, just run:
```
$ pip install django-git-storages
```

## Settings


You need to add Github credentials to `settings.py`:

```python
GIT_STORAGE = {
    'GIT_ACCESS_TOKEN': 'your_github_access_token',
    'GIT_REPO': 'username/repo',
}
```

Instead of putting credentials in `settings.py`, you can provide them as `GITHUB_ACCESS_TOKEN`,
and `GITHUB_REPO` environment variables.



Fianlly add to `settings.py`:

```python
DEFAULT_FILE_STORAGE = 'git_storage.storage.GithubStorage'
```
