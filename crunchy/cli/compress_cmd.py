"""CLI functions to compress"""
import logging
import pathlib

import click

from crunchy.compress import compress_spring

from .compare_cmd import compare
from .decompress_cmd import spring as decompress_spring_cmd

LOG = logging.getLogger(__name__)


@click.group()
def compress():
    """Compress a pair of fastq files with spring"""
    LOG.info("Running compress")


@click.command()
@click.option(
    "--first",
    "-f",
    type=click.Path(exists=True),
    required=True,
    help="First read in pair",
)
@click.option(
    "--second",
    "-s",
    type=click.Path(exists=True),
    required=True,
    help="Second read in pair",
)
@click.option(
    "--spring-path",
    "-o",
    type=click.Path(exists=False),
    required=True,
    help="Path to spring file",
)
@click.option(
    "--check-integrity",
    is_flag=True,
    help="If the integrity of the files should be checked",
)
@click.option("--dry-run", is_flag=True)
def spring(ctx, first, second, spring_path, dry_run, check_integrity):
    """Compress a pair of fastq files with spring"""
    LOG.info("Running compress spring")
    spring_api = ctx.obj.get("spring_api")
    first = pathlib.Path(first)
    second = pathlib.Path(second)
    outfile = pathlib.Path(spring_path)
    try:
        compress_spring(
            first=first,
            second=second,
            outfile=outfile,
            spring_api=spring_api,
            dry_run=dry_run,
        )
    except SyntaxError as err:
        LOG.error(err)
        raise click.Abort

    if not check_integrity:
        return

    first_spring = pathlib.Path(first).with_suffix(".spring.fastq")
    second_spring = pathlib.Path(second).with_suffix(".spring.fastq")
    ctx.invoke(
        decompress_spring_cmd,
        spring_path=spring_path,
        first=str(first_spring),
        second=str(second_spring),
        dry_run=dry_run,
    )

    success = True
    try:
        ctx.invode(compare, first=str(first), second=str(first_spring))
        ctx.invoke(compare, first=str(second), second=str(second_spring))
    except click.Abort:
        LOG.error("Uncompressed spring differ from original fastqs")
        success = False
        LOG.info("Deleting compressed spring file %s", spring_path)
        spring_path.unlink()

    LOG.info("Deleting decompressed spring files")
    first_spring.unlink()
    LOG.info("%s deleted", first_spring)
    second_spring.unlink()
    LOG.info("%s deleted", second_spring)

    if success:
        LOG.info("Files are identical, compression succesfull")
    else:
        raise click.Abort


compress.add_command(spring)
