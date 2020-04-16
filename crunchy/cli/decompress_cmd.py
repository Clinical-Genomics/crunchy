"""Code for decompress CLI fuctions"""
import logging
import pathlib

import click

from crunchy.cli.compare_cmd import compare
from crunchy.decompress import decompress_cram, decompress_spring
from crunchy.files import fastq_outpaths

LOG = logging.getLogger(__name__)


@click.group()
def decompress():
    """Decompress genomic files"""
    LOG.info("Running decompress")


@click.command()
@click.argument("spring-path", type=click.Path(exists=True))
@click.option(
    "--first",
    "-f",
    type=click.Path(exists=False),
    help="Fastq file that spring will be decompressed to. First read in pair",
)
@click.option(
    "--second",
    "-s",
    type=click.Path(exists=False),
    help="Fastq file that spring will be decompressed to. Second read in pair",
)
@click.option(
    "--first-checksum", help="Checksum from the original fastq file, first in pair",
)
@click.option(
    "--second-checksum", help="Checksum from the original fastq file, second in pair",
)
@click.option(
    "--dry-run", is_flag=True, help="Skip deleting original files",
)
@click.pass_context
def spring(ctx, spring_path, first, second, first_checksum, second_checksum, dry_run):
    """Decompress a spring file to fastq files"""
    LOG.info("Running decompress spring")
    spring_api = ctx.obj.get("spring_api")
    spring_path = pathlib.Path(spring_path)

    if not (first or second):
        LOG.warning("No filenames provided. Guess fastq file names")
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

    if not (first_checksum and second_checksum):
        LOG.info("Spring file decompressed")
        return

    try:
        ctx.invoke(compare, first=str(first), checksum=first_checksum, dry_run=dry_run)
        ctx.invoke(
            compare, first=str(second), checksum=second_checksum, dry_run=dry_run
        )
    except click.Abort:
        LOG.error("Uncompressed spring differ from given checksum")
        LOG.info("Deleting decompressed fastq files")
        first.unlink()
        second.unlink()
        raise click.Abort

    LOG.info("Spring file decompressed and verified")


@click.command()
@click.argument("cram-path", type=click.Path(exists=True))
@click.option(
    "--bam-path",
    "-b",
    type=click.Path(exists=False),
    required=True,
    help="Path to bam file",
)
@click.option(
    "--dry-run", is_flag=True, help="Skip deleting original files",
)
@click.pass_context
def cram(ctx, cram_path, bam_path, dry_run):
    """Decompress a cram file to bam file"""
    LOG.info("Running decompress cram")
    cram_api = ctx.obj.get("cram_api")
    cram_path = pathlib.Path(cram_path)
    bam_path = pathlib.Path(bam_path)

    decompress_cram(
        cram_path=cram_path, bam_path=bam_path, cram_api=cram_api, dry_run=dry_run,
    )


decompress.add_command(spring)
decompress.add_command(cram)
