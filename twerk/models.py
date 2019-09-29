from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import List

from datafiles import converters, datafile


class MonthYear(converters.Converter, datetime):
    # pylint: disable=arguments-differ,unused-argument
    @classmethod
    def to_preserialization_data(cls, python_value, **kwargs):
        return python_value.strftime("%B %Y")

    @classmethod
    def to_python_value(cls, deserialized_data, **kwargs):
        return datetime.strptime(deserialized_data, "%B %Y")


@dataclass
class Credentials:
    username: str
    password: str

    def __str__(self) -> str:
        return f"@{self.username}"

    def __repr__(self) -> str:
        masked = "▒" * len(self.password)
        return f"Credentials(username={self.username!r}, password={masked})"


@datafile("../data/accounts/{self.username}.yml", defaults=True)
class Account:
    username: str
    tweets: int = 0
    following: int = 0
    followers: int = 0
    likes: int = 0
    joined: MonthYear = MonthYear(year=2006, month=3, day=21)

    def __str__(self) -> str:
        return f"@{self.username}"


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
