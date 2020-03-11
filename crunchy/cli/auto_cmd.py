"""Code for CLI auto command"""
import logging
import pathlib

import click

from crunchy.utils import find_fastq_pairs

from .compress_cmd import fastq as compress_fastq_cmd

LOG = logging.getLogger(__name__)


@click.group()
def auto():
    """Run whole pipeline by compressing, comparing and deleting original files.
    """
    LOG.info("Running crunchy auto")


@click.command()
@click.option("--indir", type=click.Path(exists=True))
@click.option("--dry-run", is_flag=True)
@click.option("--spring-path", type=click.Path(exists=False))
@click.option(
    "--first",
    "-f",
    type=click.Path(exists=True),
    help="First in fastq pair to compare",
)
@click.option(
    "--second",
    "-s",
    type=click.Path(exists=True),
    help="Second in fastq pair to compare",
)
@click.pass_context
def spring(ctx, indir, spring_path, first, second, dry_run):
    """Run whole pipeline by compressing, comparing and deleting original fastqs.
    Either all fastq pairs below a directory or a given pair.
    """
    if indir:
        LOG.info(
            "This will recursively compress and delete fastqs in %s", indir,
        )
        indir = pathlib.Path(indir)
        if not indir.is_dir():
            LOG.warning("Please specify a directory")
            return
        pairs = find_fastq_pairs(indir)

    else:
        if not (first and second and spring_path):
            LOG.warning(
                "Please specify either a directory or two fastqs and a spring path"
            )
            return
        LOG.info(
            "Running auto, this will compress and delete fastqs %s, %s into %s",
            first,
            second,
            spring_path,
        )

        pairs = [(pathlib.Path(first), pathlib.Path(second), pathlib.Path(spring_path))]

    for pair in pairs:
        first_fastq = str(pair[0])
        second_fastq = str(pair[1])
        spring_path = str(pair[2])
        try:
            ctx.invoke(
                compress_fastq_cmd,
                first=first_fastq,
                second=second_fastq,
                spring_path=spring_path,
                dry_run=dry_run,
                check_integrity=True,
            )
        except click.Abort:
            LOG.warning("Skip current and continue auto")
            continue
