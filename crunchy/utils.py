"""Utilities for crunchy"""

import logging
import pathlib
from typing import Iterator

LOG = logging.getLogger(__name__)


def find_fastq_pairs(directory: pathlib.Path) -> Iterator[tuple]:
    """Loop over all subdirectories and return all fastq pairs found

    The function will assume the naming convention used by illumina and described in detail:
    (https://support.illumina.com/help/BaseSpace_OLH_009008/Content/Source/Informatics/BS/Naming\
     Convention_FASTQ-files-swBS.htm)

    Search for all files that have fq or fastq in its name. If found check if they are read pairs.
    Then check if both reads in pair is available.

    yields:
        tuples where first two elements are pairs and third is spring name
    """
    LOG.info("Find all pairs in %s", directory)
    valid_fastq_endings = set([".fq", ".fastq"])
    reads_found = set()
    for pth in directory.rglob("*"):
        endings = pth.suffixes
        if not set(endings).intersection(valid_fastq_endings):
            continue

        file_name = pth.name
        file_parent = pth.parent

        splitted = file_name.split("_")
        if pth in reads_found:
            LOG.debug("Read already found: %s", pth)
            continue
        if len(splitted) < 3:
            LOG.info(
                "Fastq filename %s does not follow illumina conventions", file_name
            )
            continue
        # Check if we have a part of a read pair
        spring_name = pathlib.Path("_".join(splitted[:-2]))
        if splitted[-2] in ["R1", "R2"]:
            pair_str = str(spring_name) + "_{}_" + splitted[-1]
            read_1 = pathlib.Path(file_parent, pair_str.format("R1"))
            if not read_1.exists():
                LOG.warning("Could not find first read in pair: %s", read_1)
                continue
            read_2 = pathlib.Path(file_parent, pair_str.format("R2"))
            if not read_2.exists():
                LOG.warning("Could not find second read in pair: %s", read_2)
                continue

            reads_found.add(read_1)
            reads_found.add(read_2)

            fastq_info = (
                read_1,
                read_2,
                pathlib.Path(file_parent).joinpath(spring_name).with_suffix(".spring"),
            )

            yield fastq_info
