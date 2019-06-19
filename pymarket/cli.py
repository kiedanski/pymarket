# -*- coding: utf-8 -*-

"""Console script for pymarket."""
import sys
import click


@click.command()
def main(args=None):
    """Console script for pymarket."""
    click.echo("Replace this message by putting your code into "
               "pymarket.cli.main")
    click.echo("See click documentation at http://click.pocoo.org/")
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
