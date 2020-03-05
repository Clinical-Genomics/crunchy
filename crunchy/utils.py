"""Utilities for crunchy"""

import logging
import pathlib

from .command import SpringProcess
from .compress import compress as compress_function
from .decompress import decompress as decompress_function
from .integrity import compare_elements, get_checksum

LOG = logging.getLogger(__name__)


def find_fastq_pairs(directory: pathlib.Path) -> list:
    """Loop over all subdirectories and return all fastq pairs found

    The function will assume the naming convention used by illumina and described in detail:
    (https://support.illumina.com/help/BaseSpace_OLH_009008/Content/Source/Informatics/BS/Naming\
     Convention_FASTQ-files-swBS.htm)

    Search for all files that have fq or fastq in its name. If found check if they are read pairs.
    Then check if both reads in pair is available.

    Returns:
        list of tuples where first two elements are pairs and third is spring name
    """
    LOG.info("Find all pairs in %s", directory)
    valid_fastq_endings = set([".fq", ".fastq"])
    pairs = []
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

            pairs.append(
                (
                    read_1,
                    read_2,
                    pathlib.Path(file_parent)
                    .joinpath(spring_name)
                    .with_suffix(".spring"),
                )
            )
            reads_found.add(read_1)
            reads_found.add(read_2)

    return pairs


def check_and_delete(
    first: pathlib.Path, temporary: pathlib.Path, dry_run: bool = False
) -> None:
    """Check if two files are the same. If they are delete both, otherwise only delete temporary"""
    checksums = []
    if not dry_run:
        checksums.append(get_checksum(first))
        checksums.append(get_checksum(temporary))
    else:
        checksums = [True, True]
    if compare_elements(checksums):
        LOG.info("All checksums are the same")
        LOG.info("Safely deleting fastqs")
        LOG.info("Deleting %s", first)
        if not dry_run:
            try:
                first.unlink()
                LOG.debug("%s deleted", first)
            except FileNotFoundError:
                LOG.warning("Could not find file %s", first)
    else:
        LOG.warning("All checksums are NOT the same")
        LOG.info("Will NOT delete %s", first)
    LOG.info("Deleting temp fastq %s", temporary)
    try:
        temporary.unlink()
        LOG.debug("%s deleted", temporary)
    except FileNotFoundError:
        LOG.warning("Could not find file %s", temporary)


def compress_and_delete(
    indir: pathlib.Path, spring_api: SpringProcess, dry_run: bool = True
):
    """compress and delete all fastq pairs found recursively under indir"""
    pairs = find_fastq_pairs(indir)
    for pair in pairs:
        first_in_pair = pair[0]
        second_in_pair = pair[1]
        spring_comp = pair[2]
        LOG.info(
            "Compressing %s and %s into %s", first_in_pair, second_in_pair, spring_comp
        )
        if not dry_run:
            try:
                compress_function(
                    filepath=first_in_pair,
                    second=second_in_pair,
                    outfile=spring_comp,
                    spring_api=spring_api,
                )
            except SyntaxError as err:
                LOG.warning(err)
        temp_fastq_1 = first_in_pair.with_suffix(".spring.fastq")
        temp_fastq_2 = second_in_pair.with_suffix(".spring.fastq")
        LOG.info(
            "De-Compressing spring file %s into %s and %s",
            spring_comp,
            temp_fastq_1,
            temp_fastq_2,
        )
        if not dry_run:
            try:
                decompress_function(
                    filepath=spring_comp,
                    outfile=temp_fastq_1,
                    second=temp_fastq_2,
                    spring_api=spring_api,
                )
            except SyntaxError as err:
                LOG.warning(err)

        LOG.info("Check integrity of %s and %s", first_in_pair, temp_fastq_1)
        check_and_delete(first=first_in_pair, temporary=temp_fastq_1, dry_run=dry_run)
        check_and_delete(first=second_in_pair, temporary=temp_fastq_2, dry_run=dry_run)
