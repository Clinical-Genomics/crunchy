"""Functions to decompress files"""

import gzip
import logging
import pathlib
import shutil

from .command import SpringProcess

LOG = logging.getLogger(__name__)


def build_outpaths(filepath: pathlib.Path) -> tuple:
    """Build a pair of fastq paths based on a file path"""
    stem = filepath.stem
    pair_str = str(filepath.with_suffix("")) + "_R{}_" + "001.fastq"
    return (
        pathlib.Path(stem, pair_str.format("1")),
        pathlib.Path(stem, pair_str.format("2")),
    )


def decompress_gzip(filepath: pathlib.Path, outfile: str):
    """Decompress a gzipped file"""
    LOG.info("Decompress gzipped %s to %s", filepath, outfile)
    with open(outfile, "wb") as f_out, gzip.open(filepath, "rb") as f_in:
        shutil.copyfileobj(f_in, f_out)


def decompress_spring(
    filepath: pathlib.Path, outfile: str, spring_api: SpringProcess, second: str = None
):
    """Decompress a gzipped file"""
    LOG.info("Decompress spring zipped %s to %s (and %s)", filepath, outfile, second)
    spring_api.decompress(infile=filepath, outfile=outfile, second=second)


def decompress(
    filepath: pathlib.Path,
    second: pathlib.Path = None,
    outfile: pathlib.Path = None,
    spring_api: SpringProcess = None,
):
    """Decompress a file"""
    filepath = filepath.absolute()
    ending = filepath.suffix

    if ending in [".gz", ".gzip"]:
        if not outfile:
            outfile = filepath.with_suffix("")
        outfile = outfile.absolute()
        decompress_gzip(filepath, outfile)
        return

    if ending in [".spring"]:
        if not outfile:
            LOG.warning("No filenames provided. Guess outfiles")
            fastqs = build_outpaths(filepath)
            outfile = fastqs[0]
            second = fastqs[1]
        decompress_spring(
            filepath=str(filepath),
            outfile=str(outfile),
            second=str(second),
            spring_api=spring_api,
        )
        return

    LOG.warning("Unknown file ending: %s", ending)
    LOG.info("File might not be compressed")
    raise SyntaxError
