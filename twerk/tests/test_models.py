# pylint: disable=unused-argument,unused-variable,expression-not-assigned,no-member

import pytest

from ..models import Account, Credentials


def describe_credentials():
    @pytest.fixture
    def credendials():
        return Credentials("username", "password")

    def describe_repr():
        def it_hides_password(expect, credendials):
            expect(
                repr(credendials)
            ) == "Credentials(username='username', password=▒▒▒▒▒▒▒▒)"

    def describe_str():
        def it_includes_username(expect, credendials):
            expect(str(credendials)) == "@username"


def describe_account():
    def describe_init():
        def it_defaults_to_now_for_joined(expect):
            account = Account("foobar")
            expect(account.datafile.data) == {
                "tweets": 0,
                "following": 0,
                "followers": 0,
                "likes": 0,
                "joined": "March 2006",
            }
