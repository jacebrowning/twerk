import os
from getpass import getpass

import log
from splinter import Browser
from webdriver_manager.firefox import GeckoDriverManager

from .models import Credentials


def get_browser(headless: bool = False) -> Browser:
    log.silence("selenium", "urllib3")
    options = dict(headless=headless, wait_time=1.0)
    try:
        return Browser("firefox", **options)
    except Exception as e:  # pylint: disable=broad-except
        log.debug(str(e))
        if "geckodriver" in str(e):
            path = GeckoDriverManager().install()
            return Browser("firefox", executable_path=path, **options)
        raise e from None


def get_credentials(prompt: bool = True) -> Credentials:
    username = os.getenv("TWITTER_USERNAME")
    password = os.getenv("TWITTER_PASSWORD")
    if not all((username, password)) and not prompt:
        raise EnvironmentError("Twitter credentials not available")
    username = username or input("Twitter username: ")
    password = password or getpass("Twitter password: ")
    return Credentials(username, password)


def get_seed_username() -> str:
    return os.getenv("TWITTER_SEED_USERNAME", "realDonaldTrump")
