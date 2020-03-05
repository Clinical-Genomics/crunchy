"""Tests for integrity module"""

import hashlib

from crunchy.integrity import get_checksum


def test_generate_md5(dummy_file_path):
    """Test to generate a md5"""
    # GIVEN a file and a calculated md5
    with open(dummy_file_path, "rb") as infile:
        content = infile.read()
    md5 = hashlib.md5(content).hexdigest()

    # WHEN generating a md5 from that file
    res = get_checksum(dummy_file_path, "md5")

    # THEN assert a md5 was created and returned as a string
    assert isinstance(res, str)
    # THEN the md5 is correct
    assert res == md5


def test_compare_checksums(dummy_file_path):
    """Test to compare two checksums"""
    # GIVEN a file

    # WHEN generating a checksum from that file
    res = get_checksum(dummy_file_path)
    res_2 = get_checksum(dummy_file_path)
    # THEN assert the checksums are correct
    assert res == res_2
