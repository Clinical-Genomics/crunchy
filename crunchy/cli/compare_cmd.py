"""Code for checksum module"""
import logging
import pathlib

import click

from crunchy.integrity import compare_elements, get_checksum

LOG = logging.getLogger(__name__)


@click.command()
@click.option("--first", "-f", type=click.Path(exists=True), required=True)
@click.option("--second", "-s", type=click.Path(exists=True), required=True)
@click.option(
    "--algorithm", "-a", type=click.Choice(["md5", "sha1", "sha256"]), default="sha256"
)
def compare(first, second, algorithm):
    """Compare two files by generating checksums. Fails if two files differ."""
    LOG.info("Running checksum")
    checksums = []
    for _infile in [first, second]:
        _infile = pathlib.Path(_infile)
        checksums.append(get_checksum(_infile, algorithm))

    if not compare_elements(checksums):
        LOG.warning("Checksums for %s and %s are NOT the same", first, second)
        raise click.Abort

    LOG.info("All checksums are the same")
