"""Tests for decompress functions"""

from crunchy.decompress import decompress_spring
from crunchy.files import spring_outpath


def test_decompress_spring(first_read, second_read, spring_api):
    """Test top decompress compressed file"""
    # GIVEN a compressed file and a outfile
    spring_api.decompress_success = True
    spring_path = spring_outpath(first_read)
    # WHEN decompressing
    res = decompress_spring(spring_path, first_read, second_read, spring_api)
    # THEN assert that a syntax error is raised since the file os not compressed
    assert res is True
