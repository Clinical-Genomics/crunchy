"""Tests for decompress functions."""

from pathlib import Path

from crunchy.decompress import decompress_cram, decompress_spring
from crunchy.files import spring_outpath
from tests.conftest import MockCramProcess, MockSpringProcess


def test_decompress_spring(first_read: Path, second_read: Path, spring_api: MockSpringProcess):
    """Test top decompress compressed file."""
    # GIVEN a compressed file and a outfile
    spring_path = spring_outpath(first_read)

    # WHEN decompressing
    res = decompress_spring(
        spring_path=spring_path, first=first_read, second=second_read, spring_api=spring_api
    )

    # THEN assert that the function returns True
    assert res is True


def test_decompress_spring_dry_run(
    first_read: Path, second_read: Path, spring_api: MockSpringProcess
):
    """Test top decompress compressed file."""
    # GIVEN a compressed file and a outfile
    spring_path = spring_outpath(first_read)

    # WHEN decompressing
    res = decompress_spring(
        spring_path=spring_path,
        first=first_read,
        second=second_read,
        spring_api=spring_api,
        dry_run=True,
    )

    # THEN assert that the function returns True even if no API is used
    assert res is True


def test_decompress_cram(cram_path: Path, bam_path: Path, cram_api: MockCramProcess):
    """Test to decompress a cram file,"""
    # GIVEN a cram file, a bam file and a cram api

    # WHEN decompressing
    res = decompress_cram(cram_path=cram_path, bam_path=bam_path, cram_api=cram_api)

    # THEN assert that the process return True
    assert res is True


def test_decompress_cram_dry_run(cram_path: Path, bam_path: Path, cram_api: MockCramProcess):
    """Test to decompress a cram file."""
    # GIVEN a cram file, a bam file and a cram api

    # WHEN decompressing in dry run mode
    res = decompress_cram(cram_path=cram_path, bam_path=bam_path, cram_api=cram_api, dry_run=True)

    # THEN assert that the process returns true
    assert res is True
