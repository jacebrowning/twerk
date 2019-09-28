import os
from getpass import getpass
from typing import Tuple


def get_credentials() -> Tuple[str, str]:
    username = os.getenv("TWITTER_USERNAME") or input("Twitter username: ")
    password = os.getenv("TWITTER_USERNAME") or getpass("Twitter password: ")
    return username, password


def get_seed_username() -> str:
    return os.getenv("TWITTER_SEED_USERNAME", "realDonaldTrump")
