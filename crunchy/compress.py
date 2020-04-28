"""Code to compress a pair of fastq files"""

import logging
import pathlib

from .command import CramProcess, SpringProcess

LOG = logging.getLogger(__name__)


def compress_spring(
    first_read: pathlib.Path,
    second_read: pathlib.Path,
    spring_api: SpringProcess,
    outfile: pathlib.Path,
    dry_run: bool = False,
) -> bool:
    """Compress file(s)"""
    first_read = first_read.absolute()
    second_read = second_read.absolute()
    outfile = outfile.absolute()
    LOG.info("Compressing %s and %s to %s", first_read, second_read, outfile)
    if dry_run:
        return True

    return spring_api.compress(first=first_read, second=second_read, outfile=outfile)


def compress_cram(
    bam_path: pathlib.Path,
    cram_path: pathlib.Path,
    cram_api: CramProcess,
    dry_run: bool = False,
) -> bool:
    """Compress bam file"""
    bam_path = bam_path.absolute()
    cram_path = cram_path.absolute()

    LOG.info("Compressing %s to %s", bam_path, cram_path)
    if dry_run:
        return True

    return cram_api.compress(bam_path=bam_path, cram_path=cram_path)
