"""Tests for decompress functions"""

from crunchy.decompress import decompress
from crunchy.fastq import fastq_outpaths, spring_outpath


def test_decompress(first_read, second_read, spring_api):
    """Test top decompress compressed file"""
    # GIVEN a compressed file and a outfile
    spring_api.decompress_success = True
    spring_path = spring_outpath(first_read)
    # WHEN decompressing
    res = decompress(spring_path, first_read, second_read, spring_api)
    # THEN assert that a syntax error is raised since the file os not compressed
    assert res is True


def test_decompress_real(spring_tmp, real_spring_api):
    """Test decompress a real spring file"""
    # GIVEN a spring file, a spring api and two paths to fastq files that does not exist
    assert spring_tmp.exists()
    spring_api = real_spring_api
    fastq_files = fastq_outpaths(spring_tmp)
    first_read = fastq_files[0]
    second_read = fastq_files[1]

    assert not first_read.exists()
    assert not second_read.exists()

    # WHEN decompressing the spring file to the fastq files
    res = decompress(spring_tmp, first_read, second_read, spring_api)

    # THEN assert that the fastq files have been created
    assert first_read.exists()
    assert second_read.exists()
