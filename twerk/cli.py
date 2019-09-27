"""A sample CLI."""

import click
import log
from splinter import Browser

from .models import User


@click.command(context_settings={'help_option_names': ['-h', '--help']})
@click.option(
    '--username',
    prompt='Twitter username',
    help='Username of Twitter account to automate.',
)
@click.option(
    '--password',
    prompt='Twitter password',
    hide_input=True,
    help='Password of twitter account to automate.',
)
def main(username: str = '', password: str = ''):
    log.init()

    with Browser() as browser:

        browser.visit("https://twitter.com/home")

        breakpoint()

        browser.find_by_css('.js-username-field').fill(username)
        browser.find_by_css('.js-password-field').fill(password)

        browser.find_by_text('Log in').last.click()

        browser.find_by_css('[aria-label="Profile"]').click()

        user = User.from_url(browser)

        click.echo(user)


if __name__ == '__main__':  # pragma: no cover
    main()
