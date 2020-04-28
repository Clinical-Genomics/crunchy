"""Tests for metadata module"""

from crunchy import metadata


def test_fetch_spring_metadata(first_read, second_read, spring_path):
    """Test to fetch the metadata for a spring archive"""
    # GIVEN a pair of fastq files and a spring file

    # WHEN creating the metadata
    res = metadata.fetch_spring_metadata(
        first_read=first_read, second_read=second_read, spring=spring_path
    )

    # THEN assert that the result is a list
    assert isinstance(res, list)

    # THEN assert that there is one entry per file
    assert len(res) == 3


def test_get_fastq_info(first_read):
    """Test to create metadata info for a fastq file"""
    # GIVEN a fastq file

    # WHEN fetching the file info
    res = metadata.get_fastq_info(
        fastq=first_read, tag="first_read", algorithm="sha256"
    )

    # THEN assert that the result is a dictionary
    assert isinstance(res, dict)

    # THEN assert that the checksum is there
    assert isinstance(res["checksum"], str)
