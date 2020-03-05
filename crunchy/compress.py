"""Code to compress a pair of fastq files"""

import gzip
import logging
import pathlib
import shutil

from .command import SpringProcess

LOG = logging.getLogger(__name__)


def compress_gzip(filepath: pathlib.Path, outfile: pathlib.Path):
    """Compres a file tp gzip"""
    LOG.info("Gzip %s to %s", filepath, outfile)
    with open(filepath, "rb") as f_in:
        with gzip.open(outfile, "wb") as f_out:
            shutil.copyfileobj(f_in, f_out)


def compress_spring(
    filepath: pathlib.Path,
    outfile: str,
    second: pathlib.Path = None,
    spring_api: SpringProcess = None,
):
    """Compress a fastq file with spring"""
    if second:
        LOG.info("Compress files %s, %s with spring to %s", filepath, second, outfile)
    else:
        LOG.info("Compress file %s with spring to %s", filepath, outfile)
    spring_api.compress(infile=filepath, second=second, outfile=outfile)


def compress(
    filepath: pathlib.Path,
    second: pathlib.Path = None,
    outfile: pathlib.Path = None,
    spring_api: SpringProcess = None,
):
    """Compress file(s)"""
    filepath = filepath.absolute()

    if not spring_api:
        if not outfile:
            outfile = filepath.with_suffix(filepath.suffix + ".gz")
        outfile = outfile.absolute()
        if outfile.exists():
            LOG.warning("Outfile %s already exists", outfile)
            raise SyntaxError
        compress_gzip(filepath, outfile)
        return

    if not outfile:
        LOG.warning("Please specify outfile when compressing with spring")
        raise SyntaxError

    if outfile.exists():
        LOG.warning("Outfile %s already exists", outfile)
        raise SyntaxError

    compress_spring(filepath, outfile, second, spring_api)
