"""Functions to decompress files"""

import logging
import pathlib

from .command import SpringProcess

LOG = logging.getLogger(__name__)


def decompress(
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
    return spring_api.decompress(
        spring_path=str(spring_path), first=str(first), second=str(second)
    )
