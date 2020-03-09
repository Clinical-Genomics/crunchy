"""Code for dealing with fastq paths"""

import logging
import pathlib

LOG = logging.getLogger(__name__)


def cram_outpath(bam_path: pathlib.Path) -> pathlib.Path:
    """Build a bam path based on a cram path"""
    LOG.info("Create cram path from %s", bam_path)
    file_name = bam_path.with_suffix("")
    return file_name.with_suffix(".cram")


def fastq_outpaths(filepath: pathlib.Path) -> tuple:
    """Build a pair of fastq paths based on a file path"""
    LOG.info("Create fastq paths from %s", filepath)
    file_name = filepath.name
    file_parent = filepath.parent
    pair_str = str(pathlib.Path(file_name).with_suffix("")) + "_R{}_" + "001.fastq.gz"
    return (
        pathlib.Path(file_parent, pair_str.format("1")),
        pathlib.Path(file_parent, pair_str.format("2")),
    )


def spring_outpath(filepath: pathlib.Path) -> pathlib.Path:
    """Build a spring path based on a fastq file path"""
    LOG.info("Create spring path from %s", filepath)
    file_name = filepath.name
    file_parent = filepath.parent

    splitted = file_name.split("_")
    spring_base = pathlib.Path("_".join(splitted[:-2]))

    spring_path = pathlib.Path(file_parent).joinpath(spring_base).with_suffix(".spring")
    LOG.info("Creates spring path %s", spring_path)

    return spring_path
