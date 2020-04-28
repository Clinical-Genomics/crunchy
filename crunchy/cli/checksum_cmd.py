"""Code for checksum cli command"""

import logging
import pathlib

import click

from crunchy.integrity import get_checksum

LOG = logging.getLogger(__name__)


@click.command()
@click.argument("infile", type=click.Path(exists=True))
@click.option(
    "--algorithm", "-a", type=click.Choice(["md5", "sha1", "sha256"]), default="sha256"
)
def checksum(infile, algorithm):
    """Generate the checksum for a file
    """
    LOG.info("Running checksum")
    click.echo(get_checksum(pathlib.Path(infile), algorithm))
