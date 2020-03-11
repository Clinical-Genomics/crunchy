"""Code for decompress CLI fuctions"""
import logging
import pathlib

import click

from crunchy.decompress import decompress_spring
from crunchy.files import fastq_outpaths

from .utils import file_exists

LOG = logging.getLogger(__name__)


@click.group()
def decompress():
    """Decompress genomic files"""
    LOG.info("Running decompress")


@click.command()
@click.argument("spring-path", type=click.Path(exists=True))
@click.option(
    "--first", "-f", type=click.Path(exists=False), help="First read in pair",
)
@click.option(
    "--second", "-s", type=click.Path(exists=False), help="Second read in pair",
)
@click.option(
    "--dry-run", is_flag=True, help="Skip deleting original files",
)
@click.pass_context
def spring(ctx, spring_path, first, second, dry_run):
    """Decompress a spring file to fastq files"""
    LOG.info("Running decompress")
    spring_api = ctx.obj.get("spring_api")
    spring_path = pathlib.Path(spring_path)

    if not (first or second):
        LOG.warning("No filenames provided. Guess outfiles")
        fastqs = fastq_outpaths(spring_path)
        first = fastqs[0]
        second = fastqs[1]

    first = pathlib.Path(first)
    second = pathlib.Path(second)
    if first.exists() or second.exists():
        LOG.error("Outpath(s) already exists! Specify new with '-f', '-s'")
        raise click.Abort()

    decompress_spring(
        spring_path=spring_path,
        first=first,
        second=second,
        spring_api=spring_api,
        dry_run=dry_run,
    )


decompress.add_command(spring)
