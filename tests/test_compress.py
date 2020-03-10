"""Tests for compression"""
import pathlib
import tempfile

import pytest

from crunchy.compress import compress_cram, compress_spring


def test_compress_spring_no_outpath(first_read, second_read, spring_api):
    """Test the compress function"""
    # GIVEN two files with reads from read pair, a spring api and a outfile
    # WHEN running the compression
    res = compress_spring(first=first_read, second=second_read, spring_api=spring_api)
    # THEN assert that the run was succesfull
    assert res is True


def test_compress_spring_existing_outpath(
    first_read, second_read, spring_path, spring_api
):
    """Test the compress function"""
    # GIVEN two files with reads from read pair, a spring api and a outfile that exists
    outpath = spring_path
    assert outpath.exists()
    spring_api.compress_success = True
    # WHEN running the compression
    with pytest.raises(SyntaxError):
        compress_spring(
            first=first_read, second=second_read, outfile=outpath, spring_api=spring_api
        )


def test_compress_spring(first_read, second_read, spring_api):
    """Test the compress function"""
    # GIVEN two files with reads from read pair, a spring api and a outfile
    outpath = pathlib.Path(tempfile.NamedTemporaryFile().name)
    spring_api.compress_success = True
    # WHEN running the compression
    res = compress_spring(
        first=first_read, second=second_read, outfile=outpath, spring_api=spring_api
    )
    # THEN assert that the run was succesfull
    assert res is True


def test_compress_spring_dry_run(first_read, second_read):
    """Test the compress function"""
    # GIVEN two files with reads from read pair, a spring api and a outfile
    spring_api = None
    # WHEN running the compression
    res = compress_spring(
        first=first_read, second=second_read, spring_api=spring_api, dry_run=True
    )
    # THEN assert that the run was succesfull
    assert res is True


def test_compress_cram(bam_path, cram_path, cram_api):
    """Test the compress cram function"""
    # GIVEN a bam_path, a cram path and a cram_api
    # WHEN running the compression
    res = compress_cram(bam_path=bam_path, cram_path=cram_path, cram_api=cram_api)
    # THEN assert that the run was succesfull
    assert res is True


def test_compress_cram_dry_run(bam_path, cram_path):
    """Test the compress cram function"""
    # GIVEN a bam_path, a cram path
    cram_api = None
    # WHEN running the compression
    res = compress_cram(
        bam_path=bam_path, cram_path=cram_path, cram_api=cram_api, dry_run=True
    )
    # THEN assert that the run was succesfull
    assert res is True
