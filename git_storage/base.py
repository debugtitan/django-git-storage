import os
import sys
import importlib
from operator import itemgetter

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.dispatch import receiver
from django.test.signals import setting_changed

try:
    GIT_STORAGE_CONFIG = getattr(settings, "GIT_STORAGE", {})
    GIT_ACCESS_TOKEN, GIT_REPO = itemgetter("GIT_ACCESS_TOKEN", "GIT_REPO")(
        GIT_STORAGE_CONFIG
    )
except KeyError:
    raise ImproperlyConfigured(
        "In order to use Github storage, you need to provide "
        "'GIT_STORAGE' dictionary with 'GIT_ACCESS_TOKEN' "
        "and 'GIT_REPO' in the settings (or 'GITHUB_ACCESS_TOKEN', 'GITHUB_REPO' "
        "variables)."
    )

if not GIT_ACCESS_TOKEN or not GIT_REPO:
    if not (os.environ.get("GITHUB_ACCESS_TOKEN") and os.environ.get("GITHUB_REPO")):
        raise ImproperlyConfigured(
            "In order to use Github storage, you need to provide "
            "'GIT_STORAGE' dictionary with 'GIT_ACCESS_TOKEN' "
            "and 'GIT_REPO' in the settings (or 'GITHUB_ACCESS_TOKEN', 'GITHUB_REPO' "
            "variables)."
        )

    GIT_STORAGE_CONFIG = {
        "GIT_ACCESS_TOKEN": os.environ.get("GITHUB_ACCESS_TOKEN"),
        "GIT_REPO": os.environ.get("GITHUB_REPO"),
    }


@receiver(setting_changed)
def reload_settings(*args, **kwargs):
    setting_name, value = kwargs["setting"], kwargs["value"]
    if setting_name in ["GIT_STORAGE", "MEDIA_URL"]:
        importlib.reload(sys.modules[__name__])
