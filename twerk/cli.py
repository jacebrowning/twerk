"""A sample CLI."""

import click
import log
from splinter import Browser

from .models import Account
from .views import Profile


@click.command(context_settings={"help_option_names": ["-h", "--help"]})
@click.option(
    "--username",
    prompt="Twitter username",
    help="Username of Twitter account to automate.",
)
@click.option(
    "--password",
    prompt="Twitter password",
    hide_input=True,
    help="Password of twitter account to automate.",
)
def main(username: str = "", password: str = ""):
    log.init()

    with Browser() as browser:
        account = Account.from_credentials(browser, username, password)
        profile = Profile(browser, username=account.username)
        account.tweets = profile.tweets
        click.echo(f"{account} has tweeted {account.tweets} times")


if __name__ == "__main__":  # pragma: no cover
    main()
