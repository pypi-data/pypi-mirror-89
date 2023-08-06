import logging
import sys
from exit_codes import ExitCode

import click

from intentionally_blank import api
from intentionally_blank.formatter import formatter_names

from .version import __version__

log_levels = tuple(logging._levelToName.values())

fmt_names = formatter_names()


def _validate_positive_integer(ctx, param, value):
    message = f"{param.name} needs to be a positive integer"
    try:
        float_inc = float(value)
        int_inc = int(value)
    except ValueError:
        raise click.BadParameter(message)
    if float_inc != int_inc:
        raise click.BadParameter(message)
    if int_inc < 1:
        raise click.BadParameter(message)
    return int_inc


@click.group()
@click.option(
    "--verbosity",
    default="WARNING",
    help="The logging level to use.",
    type=click.Choice(log_levels, case_sensitive=True),
)
@click.version_option(version=__version__)
def cli(verbosity):
    logging_level = getattr(logging, verbosity)
    logging.basicConfig(level=logging_level)


@cli.command(name="format")
@click.option("--format", type=click.Choice(fmt_names, case_sensitive=True), multiple=True)
@click.argument('input', type=click.File('rt'))
@click.argument('output', type=click.File('wt'))
def format(input, output, format):
    api.format_from_file_to_file(in_filepath=input, out_filepath=output, format_names=format)
    sys.exit(ExitCode.OK)


@cli.command(name="list-formatters")
def list_formatters():
    api.list_formats()
    return ExitCode.OK


@cli.command(name="describe-formatter")
@click.option("--format", type=click.Choice(fmt_names, case_sensitive=True))
def describe_formatter(format):
    api.describe_formatter(format_name=format)
    return ExitCode.OK


if __name__ == "__main__":
    cli()

