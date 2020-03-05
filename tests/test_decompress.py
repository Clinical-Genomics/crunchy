"""Tests for decompress functions"""
import tempfile

import pytest

from crunchy.decompress import decompress


def test_decompress_uncompressed(dummy_file_path):
    """Test top decompress uncompressed file"""
    # GIVEN a uncompressed file
    # WHEN decompressing
    with pytest.raises(SyntaxError):
        # THEN assert that a syntax error is raised since the file os not compressed
        decompress(dummy_file_path)


def test_decompress_compressed(zipped_file_path):
    """Test top decompress compressed file"""
    # GIVEN a compressed file and a outfile
    outfile_obj = tempfile.NamedTemporaryFile()
    outfile = outfile_obj.name
    # WHEN decompressing
    decompress(zipped_file_path, outfile)
    # THEN assert that a syntax error is raised since the file os not compressed
    with open(outfile, "r") as content:
        for line in content:
            if len(line) > 0:
                assert line.strip() == "This is stupid"
