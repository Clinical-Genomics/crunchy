"""Code for checksum module."""
import logging
import pathlib

import click

from crunchy.integrity import compare_elements, get_checksum

LOG = logging.getLogger(__name__)


@click.command()
@click.option("--first", "-f", type=click.Path(exists=True), required=True)
@click.option("--second", "-s", type=click.Path(exists=True))
@click.option(
    "--checksum", "-c", help="If the file should be compared to a checksum directly",
)
@click.option(
    "--algorithm", "-a", type=click.Choice(["md5", "sha1", "sha256"]), default="sha256"
)
@click.option("--dry-run", is_flag=True)
def compare(first, second, algorithm, checksum, dry_run):
    """Compare two files by generating checksums. Fails if two files differ.

    Either the checksum of two files can be compared. Files will be decompressed and checksums
    calculated. Or the checksum of a file can be compared to a checksum string given on the command
    line. Use --first and --checksum if a file should be compared directly to a checksum.
    """
    LOG.info("Running checksum")
    if second and checksum:
        LOG.error("Use --first only in combination with --checksum")
        raise click.Abort

    if dry_run:
        LOG.info("Dry Run!")

    checksums = []
    if checksum:
        checksums.append(checksum)

    for _infile in [first, second]:
        if not _infile:
            continue
        if dry_run:
            checksums.append("dummy_checksum")
            continue
        _infile = pathlib.Path(_infile)
        checksums.append(get_checksum(_infile, algorithm))

    if not dry_run and not compare_elements(checksums):
        LOG.warning(f"Checksums for {first} and {second} are NOT the same")
        raise click.Abort

    LOG.info(f"Checksum: {checksums[0]}")
    LOG.info("All checksums are the same")
