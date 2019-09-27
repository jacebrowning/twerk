from __future__ import annotations

from typing import Optional

import log
from datafiles import datafile
from splinter import Browser
from splinter.exceptions import ElementDoesNotExist


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

        browser.find_by_css(".js-username-field").fill(username)
        browser.find_by_css(".js-password-field").fill(password)

        browser.find_by_text("Log in").last.click()

        browser.find_by_css('[aria-label="Profile"]').click()

        account = cls.from_url(browser)
        assert account, f"Failed to login to account: {username}"

        return account
