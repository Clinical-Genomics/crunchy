"""Code to test crunchys files module"""
import pathlib

from crunchy import files


def test_cram_output():
    """Test to generate a cram path from bam"""
    # GIVEN a bam path
    abam = pathlib.Path("test.bam")
    # WHEN fetching the cram path
    acram = files.cram_outpath(abam)
    # THEN assert the filename is the same
    assert abam.with_suffix("") == acram.with_suffix("")
    assert str(abam) != str(acram)
