import requests
from .load_repository import load_repository_name, load_repository_organization


def travis_project_exists() -> bool:
    """Return boolean representing if given travis project exists."""
    return "unknown" not in requests.get(
        "https://api.travis-ci.org/{account}/{repository}.svg".format(
            account=load_repository_organization(),
            repository=load_repository_name()
        )
    ).text
