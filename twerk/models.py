from __future__ import annotations

import time
from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional

import log
from datafiles import datafile
from splinter import Browser
from splinter.exceptions import ElementDoesNotExist


@dataclass
class Account:
    username: str
    tweets: int = 0
    following: int = 0
    followers: int = 0
    joined: datetime = datetime(year=2006, month=3, day=21)

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


@dataclass
class Bot:
    username: str
    account_age: str
    tweet_count: int
    tweets_per_hour: float
    follower_count: int

    def __str__(self) -> str:
        return (
            f"@{self.username} is {self.account_age} old"
            f" and had tweeted {self.tweet_count}"
            f" at a rate of {self.tweets_per_hour} tweets/hour"
            f" with {self.follower_count} followers"
        )


@datafile("../data/blocklist.json", defaults=True)
class Bots:
    bots: List[Bot]
