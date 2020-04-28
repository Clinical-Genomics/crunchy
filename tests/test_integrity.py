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


def test_generate_sha1(dummy_file_path):
    """Test to generate a sha1 checksum"""
    # GIVEN a file and a calculated sha1
    with open(dummy_file_path, "rb") as infile:
        content = infile.read()
    sha1 = hashlib.sha1(content).hexdigest()

    # WHEN generating a sha1 from that file
    res = get_checksum(dummy_file_path, "sha1")

    # THEN assert a sha1 was created and returned as a string
    assert isinstance(res, str)
    # THEN the sha1 is correct
    assert res == sha1


def test_compare_checksums(dummy_file_path):
    """Test to compare two checksums"""
    # GIVEN a file

    # WHEN generating a checksum from that file
    res = get_checksum(dummy_file_path)
    res_2 = get_checksum(dummy_file_path)
    # THEN assert the checksums are correct
    assert res == res_2


def test_generate_checksum_read_1(first_read, checksum_first_read):
    """Test to generate checksum for a fastq file"""
    # GIVEN a fastq file and the corresponding sha256 checksum

    # WHEN generating a checksum for that fastq file
    res = get_checksum(first_read)

    # THEN assert that the checksums are the same
    assert res == checksum_first_read
