"""A sample CLI."""

import click
import ipdb
import log
from splinter import Browser

from .models import Account, Credentials
from .utils import get_browser
from .views.private import Profile


@click.command(context_settings={"help_option_names": ["-h", "--help"]})
@click.option(
    "--username",
    envvar="TWITTER_USERNAME",
    prompt="Twitter username",
    help="Username of Twitter account to automate.",
)
@click.option(
    "--password",
    envvar="TWITTER_PASSWORD",
    prompt="Twitter password",
    hide_input=True,
    help="Password of twitter account to automate.",
)
@click.option("--debug", is_flag=True)
def main(username: str = "", password: str = "", debug: bool = False):
    log.init(debug=debug)
    log.silence("datafiles")

    with get_browser() as browser:
        try:
            run(browser, username, password)
        except Exception as e:  # pylint: disable=broad-except
            if debug:
                log.exception(e)
                ipdb.post_mortem()
            else:
                raise e from None


def run(browser: Browser, username: str = "", password: str = ""):
    credentials = Credentials(username, password)
    profile = Profile(browser, username=username, credentials=credentials)
    account = Account(username, tweets=profile.tweets)
    click.echo(f"{account} has tweeted {account.tweets} times")


if __name__ == "__main__":  # pragma: no cover
    main()
