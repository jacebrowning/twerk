import os
from getpass import getpass

from splinter import Browser

from .models import Credentials


def get_browser() -> Browser:
    return Browser(wait_time=1.0)


def get_credentials() -> Credentials:
    username = os.getenv("TWITTER_USERNAME") or input("Twitter username: ")
    password = os.getenv("TWITTER_PASSWORD") or getpass("Twitter password: ")
    return Credentials(username, password)


def get_seed_username() -> str:
    return os.getenv("TWITTER_SEED_USERNAME", "realDonaldTrump")
