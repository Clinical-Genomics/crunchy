"""Tests for compression."""
import pathlib
import tempfile

from crunchy.command import CramProcess, SpringProcess
from crunchy.compress import compress_cram, compress_spring



def test_compress_spring(first_read, second_read, spring_api: SpringProcess):
    """Test the compress function."""
    # GIVEN two files with reads from read pair, a spring api and a outfile
    outpath = pathlib.Path(tempfile.NamedTemporaryFile().name)
    spring_api.compress_success = True
    # WHEN running the compression
    res = compress_spring(
        first_read=first_read,
        second_read=second_read,
        outfile=outpath,
        spring_api=spring_api,
    )
    # THEN assert that the run was successfull
    assert res is True


def test_compress_spring_dry_run(first_read, second_read, spring_api: SpringProcess):
    """Test the compress function."""
    # GIVEN two files with reads from read pair, a spring api and a outfile
    outpath = pathlib.Path(tempfile.NamedTemporaryFile().name)
    # WHEN running the compression
    res = compress_spring(
        first_read=first_read,
        second_read=second_read,
        outfile=outpath,
        spring_api=spring_api,
        dry_run=True,
    )
    # THEN assert that the run was successful
    assert res is True


def test_compress_cram(bam_path, cram_path, cram_api):
    """Test the compress cram function"""
    # GIVEN a bam_path, a cram path and a cram_api
    # WHEN running the compression
    res = compress_cram(bam_path=bam_path, cram_path=cram_path, cram_api=cram_api)
    # THEN assert that the run was successfull
    assert res is True


def test_compress_cram_dry_run(bam_path, cram_api: CramProcess, cram_path):
    """Test the compress cram function"""
    # GIVEN a bam_path, a cram path

    # WHEN running the compression
    res = compress_cram(
        bam_path=bam_path, cram_path=cram_path, cram_api=cram_api, dry_run=True
    )
    # THEN assert that the run was successfull
    assert res is True
