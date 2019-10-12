"""A sample CLI."""

import click
import log

from . import commands
from .utils import get_browser


@click.group(context_settings={"help_option_names": ["-h", "--help"]})
def main():
    log.init()
    log.silence("datafiles")


@main.command(help="Verify browser automation is working.")
@click.option(
    "--username",
    envvar="TWITTER_USERNAME",
    prompt="Twitter username",
    help="Username of Twitter account to automate.",
)
@click.option("--debug", is_flag=True, help="Start debugger on exceptions.")
def check(username: str, debug: bool):
    with get_browser() as browser:
        try:
            commands.check(browser, username, display=click.echo)
        except Exception as e:  # pylint: disable=broad-except
            if debug:
                import ipdb  # pylint: disable=import-outside-toplevel

                log.exception(e)

                ipdb.post_mortem()
            else:
                raise e from None


@main.command(help="Crawl for bots starting from seed account.")
@click.argument("username", envvar="TWITTER_SEED_USERNAME")
def crawl(username: str):
    with get_browser() as browser:
        commands.crawl(browser, username)


@main.command(help="Verify browser automation is working.")
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
def block(username: str, password: str):
    with get_browser() as browser:
        commands.block(browser, username, password, display=click.echo)


if __name__ == "__main__":  # pragma: no cover
    main()
