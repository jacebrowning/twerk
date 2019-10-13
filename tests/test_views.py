# pylint: disable=redefined-outer-name,unused-variable,expression-not-assigned

import pytest

from twerk import utils
from twerk.views import private, public


@pytest.fixture(scope="module")
def browser():
    with utils.get_browser(headless=True) as browser:
        yield browser


@pytest.fixture
def credentials():
    try:
        return utils.get_credentials(prompt=False)
    except EnvironmentError as e:
        pytest.skip(str(e))


def describe_public_views():
    def describe_profile():
        @pytest.fixture(scope="module")
        def profile(browser):
            return public.Profile(browser, username="jack")

        @pytest.mark.flaky
        def it_contains_properties(expect, profile):
            expect(profile.tweets) > 0
            expect(profile.following) > 0
            expect(profile.followers) > 0
            expect(profile.likes) > 0
            expect(profile.joined) != None


def describe_private_views():
    def describe_profile():
        @pytest.fixture
        def profile(browser, credentials):
            return private.Profile(browser, username="jack", credentials=credentials)

        @pytest.mark.flaky
        def it_contains_properties(expect, profile):
            expect(profile.tweets) > 0
            expect(profile.following) > 0
            expect(profile.followers) > 0
            expect(profile.likes) == 0  # not yet supported
            expect(profile.joined) != None

    def describe_profile_block():
        @pytest.fixture
        def profile_block(browser, credentials):
            return private.ProfileBlock(
                browser, username="jack", credentials=credentials
            )

        @pytest.mark.flaky
        def it_can_cancel(expect, profile_block):
            view = profile_block.cancel()
            expect(view).isinstance(private.Profile)

    def describe_profile_report():
        @pytest.fixture
        def profile_report(browser, credentials):
            return private.ProfileReport(
                browser, username="jack", credentials=credentials
            )

        @pytest.mark.flaky
        def it_can_cancel(expect, profile_report):
            view = profile_report.cancel()
            expect(view).isinstance(private.Profile)
