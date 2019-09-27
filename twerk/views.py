from __future__ import annotations

import re
from abc import ABC, abstractmethod

from splinter import Browser


class View(ABC):
    def __init__(self, browser: Browser, *username: str, goto: bool = True):
        self._browser = browser
        self.username = username

        if self._active:
            return

        if goto:
            self._goto()

        raise RuntimeError(f'Expected {self} to already be active')

    @property
    def _url(self) -> str:
        return f"https://twitter.com/{self.username}"

    @property
    def _active(self) -> bool:
        return self._browser.url == self._url

    @abstractmethod
    def _goto(self) -> View:
        raise NotImplementedError


class Profile(View):
    def _goto(self) -> Profile:
        self._browser.visit(self._url)
        return self

    @property
    def tweets(self) -> int:
        match = re.search(r'([\d.]+)(K?) Tweets', self._browser.html)
        assert match
        count = float(match.group(1))
        if match.group(2):
            count *= 1000
        return int(count)

    def more(self) -> ProfileMore:
        self._browser.find_by_css('[aria-label="More"]').click()
        return ProfileMore(self.username, self._browser)


class ProfileMore(View):
    @property
    def _active(self) -> bool:
        return self._browser.url == self._url and self._browser.is_text_present(
            "Add/remove from Lists"
        )

    def _goto(self) -> ProfileMore:
        return Profile(self.username, self._browser).more()

    def block(self) -> ProfileBlock:
        self._browser.find_by_text(f"Block @{self.username}").click()
        return ProfileBlock(self.username, self._browser)


class ProfileBlock(View):
    @property
    def _active(self) -> bool:
        return self._browser.url == self._url and self._browser.is_text_present(
            "They will not be able to follow you"
        )

    def _goto(self) -> ProfileBlock:
        return ProfileMore(self.username, self._browser).block()

    def cancel(self):
        self._browser.find_by_text("Cancel").click()
        return Profile(self.username, self._browser)

    def block(self):
        self._browser.find_by_text("Block").click()
        return Profile(self.username, self._browser)
