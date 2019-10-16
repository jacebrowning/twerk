import os
from getpass import getpass

import log
from splinter import Browser
from webdriver_manager import chrome, firefox

from .models import Credentials


WEBDRIVER_MANAGERS = {
    "chromedriver": chrome.ChromeDriverManager,
    "geckodriver": firefox.GeckoDriverManager,
}


def get_browser(name: str = "", headless: bool = False) -> Browser:
    log.silence("selenium", "urllib3")

    name = name.lower()
    options = {"headless": headless, "wait_time": 1.0}

    try:
        return Browser(name, **options) if name else Browser(**options)
    except Exception as e:  # pylint: disable=broad-except
        log.debug(str(e))

        for driver, manager in WEBDRIVER_MANAGERS.items():
            if driver in str(e):
                options["executable_path"] = manager().install()
                return Browser(name, **options) if name else Browser(**options)

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
