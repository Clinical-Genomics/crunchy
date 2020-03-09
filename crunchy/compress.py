"""Code to compress a pair of fastq files"""

import logging
import pathlib

from .command import SpringProcess
from .files import spring_outpath

LOG = logging.getLogger(__name__)


def compress_spring(
    first: pathlib.Path,
    second: pathlib.Path,
    spring_api: SpringProcess,
    outfile: pathlib.Path = None,
    dry_run: bool = False,
) -> bool:
    """Compress file(s)"""
    first = first.absolute()
    second = second.absolute()

    if not outfile:
        LOG.warning("No spring outpath specified.")
        outfile = spring_outpath(first)

    if outfile.exists():
        raise SyntaxError("Outfile {} already exists".format(outfile))

    outfile = outfile.absolute()
    LOG.info("Compressing %s and %s to %s", first, second, outfile)
    if dry_run:
        return True

    return spring_api.compress(first=first, second=second, outfile=outfile)


def compress_cram(
    bam_path: pathlib.Path,
    cram_path: pathlib.Path,
    cram_api: SpringProcess,
    dry_run: bool = False,
) -> bool:
    """Compress bam file"""
    bam_path = bam_path.absolute()
    cram_path = cram_path.absolute()

    LOG.info("Compressing %s to %s", bam_path, cram_path)
    if dry_run:
        return True

    return cram_api.compress(bam_path=str(bam_path), cram_path=str(cram_path))
