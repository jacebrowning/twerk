# pylint: disable=unused-argument,unused-variable,expression-not-assigned,no-member


from dataclasses import asdict
from datetime import datetime

from ..models import Account


def describe_account():
    def describe_init():
        def it_defaults_to_now_for_joined(expect):
            account = Account("foobar")
            expect(asdict(account)) == {
                "username": "foobar",
                "tweets": 0,
                "following": 0,
                "followers": 0,
                "joined": datetime(2006, 3, 21, 0, 0),
            }
