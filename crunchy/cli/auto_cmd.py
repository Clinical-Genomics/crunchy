"""Code for CLI auto command"""
import logging
import pathlib

import click

from crunchy.utils import find_fastq_pairs

from .compress_cmd import fastq as compress_fastq_cmd

LOG = logging.getLogger(__name__)


def abort_if_false(ctx, param, value):
    """Check if abort"""
    if not value:
        ctx.abort()


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
@click.option(
    "--yes",
    is_flag=True,
    callback=abort_if_false,
    expose_value=False,
    prompt="Are you sure you want to compress and delete all fastqs",
)
@click.pass_context
def fastq(ctx, indir, spring_path, first, second, dry_run):
    """Run whole pipeline by compressing, comparing and deleting original fastqs.
    Either all fastq pairs below a directory or a given pair.
    """
    if dry_run:
        LOG.info("Dry Run! No files will be created or deleted")

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
        first_fastq = pair[0]
        second_fastq = pair[1]
        spring_path = pair[2]
        try:
            ctx.invoke(
                compress_fastq_cmd,
                first_read=str(first_fastq),
                second_read=str(second_fastq),
                spring_path=str(spring_path),
                dry_run=dry_run,
                check_integrity=True,
            )
        except click.Abort:
            LOG.warning("Skip current and continue auto")
            continue

        LOG.info("Deleting original fastqs")
        if not dry_run:
            first_fastq.unlink()
            LOG.info("%s deleted", first_fastq)
            second_fastq.unlink()
            LOG.info("%s deleted", second_fastq)

    LOG.info("crunchy auto fastq completed")


auto.add_command(fastq)
