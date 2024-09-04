"""Tests for the command module"""


def test_get_index_path_cram(cram_api, cram_tmp_path):
    """test to create a index path"""
    # GIVEN a cram path and a cram api
    assert cram_tmp_path.suffix == ".cram"
    # WHEN creating a index
    index = cram_api.get_index_path(cram_tmp_path)
    # THEN assert that the index has the correct suffix
    assert index.suffix == ".crai"
    assert set(index.suffixes) == set([".cram", ".crai"])


def test_get_index_path_bam(cram_api, bam_tmp_path):
    """test to create a index path"""
    # GIVEN a bam path and a cram api
    assert bam_tmp_path.suffix == ".bam"
    # WHEN creating a index
    index = cram_api.get_index_path(bam_tmp_path)
    # THEN assert that the index has the correct suffix
    assert index.suffix == ".bai"
    assert set(index.suffixes) == set([".bam", ".bai"])
