"""Tests for decompress functions"""

from crunchy.decompress import decompress_cram, decompress_spring
from crunchy.files import spring_outpath


def test_decompress_spring(first_read, second_read, spring_api):
    """Test top decompress compressed file"""
    # GIVEN a compressed file and a outfile
    spring_path = spring_outpath(first_read)
    # WHEN decompressing
    res = decompress_spring(spring_path, first_read, second_read, spring_api)
    # THEN assert that a the function returns True
    assert res is True


def test_decompress_spring_dry_run(first_read, second_read):
    """Test top decompress compressed file"""
    # GIVEN a compressed file and a outfile
    spring_api = None
    spring_path = spring_outpath(first_read)
    # WHEN decompressing
    res = decompress_spring(
        spring_path, first_read, second_read, spring_api, dry_run=True
    )
    # THEN assert that the function returns True even if no api is used
    assert res is True


def test_decompress_cram(cram_path, bam_path, cram_api):
    """Test to decompress a cram file"""
    # GIVEN a cram file, a bam file and a cram api
    # WHEN decompressing
    res = decompress_cram(cram_path=cram_path, bam_path=bam_path, cram_api=cram_api)
    # THEN assert that the process succeeds
    assert res is True


def test_decompress_cram_dry_run(cram_path, bam_path):
    """Test to decompress a cram file"""
    # GIVEN a cram file, a bam file and a cram api
    cram_api = None
    # WHEN decompressing
    res = decompress_cram(
        cram_path=cram_path, bam_path=bam_path, cram_api=cram_api, dry_run=True
    )
    # THEN assert that the process succeeds even without an api
    assert res is True
