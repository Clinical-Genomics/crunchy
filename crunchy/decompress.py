"""Functions to decompress files."""

import logging
from pathlib import Path

from .command import CramProcess, SpringProcess

LOG = logging.getLogger(__name__)


def decompress_spring(
    spring_path: Path,
    first: Path,
    second: Path,
    spring_api: SpringProcess,
    dry_run: bool = False,
) -> bool:
    """Decompress a spring file into two fastq files."""
    spring_path = spring_path.absolute()
    first = first.absolute()
    second = second.absolute()
    LOG.info(f"Decompressing {spring_path} to {first} and {second}")
    if dry_run:
        return True
    return spring_api.decompress(spring_path=spring_path, first=first, second=second)


def decompress_cram(
    cram_path: Path,
    bam_path: Path,
    cram_api: CramProcess,
    dry_run: bool = False,
) -> bool:
    """Decompress a cram file into a bam file."""
    cram_path = cram_path.absolute()
    bam_path = bam_path.absolute()
    LOG.info(f"Decompressing {cram_path} to {bam_path}")
    if dry_run:
        return True
    return cram_api.decompress(cram_path=cram_path, bam_path=bam_path)
