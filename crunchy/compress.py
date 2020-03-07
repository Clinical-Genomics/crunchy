"""Code to compress a pair of fastq files"""

import logging
import pathlib

from .command import SpringProcess
from .fastq import spring_outpath

LOG = logging.getLogger(__name__)


def compress(
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
