"""Tests for compression"""
import pathlib
import tempfile

from crunchy.compress import compress


def test_compress(first_read, second_read, spring_api):
    """Test the compress function"""
    # GIVEN two files with reads from read pair, a spring api and a outfile
    outpath = pathlib.Path(tempfile.NamedTemporaryFile().name)
    spring_api.compress_success = True
    # WHEN running the compression
    res = compress(
        first=first_read, second=second_read, outfile=outpath, spring_api=spring_api
    )
    # THEN assert that the run was succesfull
    assert res is True
