"""CLI functions to compress."""
import logging
from pathlib import Path
from typing import Optional

import click

from crunchy.cli.compare_cmd import compare
from crunchy.cli.decompress_cmd import spring as decompress_spring_cmd
from crunchy.cli.utils import file_exists
from crunchy.compress import compress_cram, compress_spring
from crunchy.files import cram_outpath, spring_outpath
from crunchy.metadata import dump_spring_metadata, fetch_spring_metadata

LOG = logging.getLogger(__name__)


@click.group()
def compress():
    """Compress genomic files."""


@click.command()
@click.option(
    "--first-read",
    "-f",
    type=click.Path(exists=True),
    required=True,
    help="First read in pair",
)
@click.option(
    "--second-read",
    "-s",
    type=click.Path(exists=True),
    required=True,
    help="Second read in pair",
)
@click.option(
    "--spring-path", "-o", help="Path to spring file",
)
@click.option(
    "--check-integrity",
    is_flag=True,
    help="If the integrity of the files should be checked",
)
@click.option("--dry-run", is_flag=True)
@click.option(
    "--metadata-file",
    is_flag=True,
    help="If a json file with metada should be produced",
)
@click.pass_context
def fastq(
    ctx, first_read, second_read, spring_path, dry_run, check_integrity, metadata_file
):
    """Compress a pair of FASTQ files with Spring."""
    LOG.info("Running compress fastq")
    if dry_run:
        LOG.warning("Dry Run! No files will be created or deleted")

    spring_api = ctx.obj.get("spring_api")
    first_read = Path(first_read)
    second_read = Path(second_read)
    spring_path = Path(spring_path) if spring_path else spring_outpath(first_read)

    file_exists(spring_path, exists=False)

    compress_spring(
        first_read=first_read,
        second_read=second_read,
        outfile=spring_path,
        spring_api=spring_api,
        dry_run=dry_run,
    )

    metadata = fetch_spring_metadata(
        first_read=first_read, second_read=second_read, spring=spring_path
    )

    metadata_path: Optional[Path]= dump_spring_metadata(metadata) if metadata_file else None
    if not check_integrity:
        return

    first_spring = Path(first_read).with_suffix(".spring.fastq")
    second_spring = Path(second_read).with_suffix(".spring.fastq")

    ctx.invoke(
        decompress_spring_cmd,
        spring_path=str(spring_path),
        first_read=str(first_spring),
        second_read=str(second_spring),
        dry_run=dry_run,
    )

    checksums = [None, None]
    for file_info in metadata:
        if file_info["file"] == "first_read":
            checksums[0] = file_info["checksum"]
        elif file_info["file"] == "second_read":
            checksums[1] = file_info["checksum"]

    success = True
    try:
        ctx.invoke(
            compare, first=str(first_spring), checksum=checksums[0], dry_run=dry_run
        )
        ctx.invoke(
            compare, first=str(second_spring), checksum=checksums[1], dry_run=dry_run
        )
    except click.Abort:
        LOG.error("Uncompressed Spring differ from original FASTQs")
        success = False
        LOG.info(f"Deleting compressed spring file {spring_path}")
        spring_path.unlink()
        if metadata_file:
            LOG.info(f"Deleting metadata file {metadata_path}")
            metadata_path.unlink()

    LOG.info("Deleting decompressed spring files")
    if not dry_run:
        first_spring.unlink()
        LOG.info(f"{first_spring} deleted")
        second_spring.unlink()
        LOG.info(f"{second_spring} deleted")

    if not success:
        raise click.Abort
    LOG.info("Files are identical, compression successful")


@click.command()
@click.option(
    "--bam-path",
    "-b",
    type=click.Path(exists=True),
    required=True,
    help="Path to bam file",
)
@click.option(
    "--cram-path", "-c", help="Path to cram file",
)
@click.option("--dry-run", is_flag=True)
@click.pass_context
def bam(ctx, bam_path: click.Path, cram_path: str, dry_run: bool):
    """Compress a BAM file to CRAM format with Samtools."""
    LOG.info("Running compress BAM")
    if dry_run:
        LOG.info("Dry Run! No files will be created or deleted")
    cram_api = ctx.obj.get("cram_api")
    try:
        cram_api.self_check()
    except (SyntaxError, FileNotFoundError) as error:
        raise click.Abort from error
    bam_path: Path = Path(bam_path)
    cram_path: Path = Path(cram_path) if cram_path else cram_outpath(bam_path)
    file_exists(cram_path, exists=False)
    compress_cram(
        bam_path=bam_path, cram_path=cram_path, cram_api=cram_api, dry_run=dry_run,
    )

    LOG.info("Compression successful")


for sub_cmd in [fastq, bam]:
    compress.add_command(sub_cmd)

