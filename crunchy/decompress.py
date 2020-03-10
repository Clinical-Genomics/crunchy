"""Functions to decompress files"""

import logging
import pathlib

from .command import CramProcess, SpringProcess

LOG = logging.getLogger(__name__)


def decompress_spring(
    spring_path: pathlib.Path,
    first: pathlib.Path,
    second: pathlib.Path,
    spring_api: SpringProcess,
    dry_run: bool = False,
) -> bool:
    """Decompress a spring file into two fastq files"""
    spring_path = spring_path.absolute()
    first = first.absolute()
    second = second.absolute()
    LOG.info("Decompressing %s to %s and %s", spring_path, first, second)
    if dry_run:
        return True

    return spring_api.decompress(spring_path=spring_path, first=first, second=second)


def decompress_cram(
    cram_path: pathlib.Path,
    bam_path: pathlib.Path,
    cram_api: CramProcess,
    dry_run: bool = False,
) -> bool:
    """Decompress a cram file into a bam file"""
    cram_path = cram_path.absolute()
    bam_path = bam_path.absolute()
    LOG.info("Decompressing %s to %s", cram_path, bam_path)
    if dry_run:
        return True

    return cram_api.decompress(cram_path=cram_path, bam_path=bam_path)
