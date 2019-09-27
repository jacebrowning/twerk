# pylint: disable=redefined-outer-name,unused-variable,expression-not-assigned

import pytest
from click.testing import CliRunner
from expecter import expect

from twerk.cli import main


@pytest.fixture
def runner():
    return CliRunner()


def describe_cli():
    def describe_help():
        def placeholder(runner):
            result = runner.invoke(main, ['--help'])

            expect(result.exit_code) == 0
            expect(result.output).contains("Show this message and exit.")
