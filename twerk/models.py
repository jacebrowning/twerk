from __future__ import annotations

import time
from datetime import datetime
from typing import Optional

import log
from splinter import Browser
from splinter.exceptions import ElementDoesNotExist

from datafiles import converters, datafile


class MonthYear(converters.Converter, datetime):
    # pylint: disable=arguments-differ,unused-argument
    @classmethod
    def to_preserialization_data(cls, python_value, **kwargs):
        return python_value.strftime("%B %Y")

    @classmethod
    def to_python_value(cls, deserialized_data, **kwargs):
        return datetime.strptime(deserialized_data, "%B %Y")


@datafile("../data/accounts/{self.username}.yml")
class Account:
    username: str
    tweets: int = 0

    def __str__(self) -> str:
        return f"@{self.username}"

    @classmethod
    def from_url(cls, browser: Browser) -> Optional[Account]:
        browser.visit("https://twitter.com/home")
        try:
            browser.find_by_css('[aria-label="Profile"]').first.click()
        except ElementDoesNotExist:
            log.error("Please log in first")
            return None
        else:
            username = browser.url.split("/")[-1]
            return cls(username)

    @classmethod
    def from_credentials(
        cls, browser: Browser, username: str, password: str
    ) -> Account:
        browser.visit("https://twitter.com/home")

        log.debug(f"Filling username: {username}")
        browser.find_by_css(".js-username-field").first.fill(username)

        time.sleep(0.5)

        log.debug(f"Filling password: {'*' * len(password)}")
        browser.find_by_css(".js-password-field").first.fill(password)

        browser.find_by_text("Log in").last.click()

        browser.find_by_css('[aria-label="Profile"]').click()

        account = cls.from_url(browser)
        assert account, f"Failed to login to account: {username}"

        return account


@datafile("../data/bots/{self.username}.yml", defaults=True)
class Bot:
    username: str
    tweets: int = 0
    following: int = 0
    followers: int = 0
    joined: MonthYear = MonthYear(year=2006, month=3, day=21)
