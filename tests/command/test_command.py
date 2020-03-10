"""Tests for the command module"""
import pathlib

from crunchy.files import fastq_outpaths


def test_compress_spring(spring_tmp_path, first_tmp_file, second_tmp_file, spring_api):
    """Test compress a a fastq pair with spring"""
    # GIVEN a spring api
    # GIVEN two existing fastq reads
    assert first_tmp_file.exists()
    assert second_tmp_file.exists()
    # GIVEN a spring path that does not exist
    assert not spring_tmp_path.exists()

    # WHEN compressing fastq files into the spring file
    res = spring_api.compress(
        str(first_tmp_file), str(second_tmp_file), str(spring_tmp_path)
    )

    # THEN assert that process was succesful
    assert res is True
    # THEN assert that the spring compression exists
    assert spring_tmp_path.exists()


def test_decompress_spring(spring_tmp_file, spring_api):
    """Test decompress a real spring file"""
    # GIVEN a spring file, a spring api and two paths to fastq files that does not exist
    assert spring_tmp_file.exists()
    fastq_files = fastq_outpaths(spring_tmp_file)
    first_read = fastq_files[0]
    second_read = fastq_files[1]

    assert not first_read.exists()
    assert not second_read.exists()

    # WHEN decompressing the spring file to the fastq files
    res = spring_api.decompress(str(spring_tmp_file), str(first_read), str(second_read))

    # THEN assert that the fastq files have been created
    assert res is True
    assert first_read.exists()
    assert second_read.exists()


def test_decompress_cram(cram_tmp_file, bam_tmp_path, cram_api):
    """Test decompress a real cram file"""
    # GIVEN a existing cram file
    assert cram_tmp_file.exists()
    # GIVEN a non existing bam path
    assert not bam_tmp_path.exists()
    # GIVEN a cram api

    # WHEN decompressing the cram file
    res = cram_api.decompress(str(cram_tmp_file), str(bam_tmp_path))

    # THEN assert that the process executed with success
    assert res is True
    # THEN assert that the bam file was created
    assert bam_tmp_path.exists()


def test_get_index_path_cram(cram_api, cram_tmp_path):
    """test to create a index path"""
    # GIVEN a cram path and a cram api
    assert cram_tmp_path.suffix == ".cram"
    # WHEN creating a index
    index = cram_api.get_index_path(str(cram_tmp_path))
    # THEN assert that the index has the correct suffix
    assert index.endswith(".crai")
    assert set(pathlib.Path(index).suffixes) == set([".cram", ".crai"])


def test_get_index_path_bam(cram_api, bam_tmp_path):
    """test to create a index path"""
    # GIVEN a bam path and a cram api
    assert bam_tmp_path.suffix == ".bam"
    # WHEN creating a index
    index = cram_api.get_index_path(str(bam_tmp_path))
    # THEN assert that the index has the correct suffix
    assert index.endswith(".bai")
    assert set(pathlib.Path(index).suffixes) == set([".bam", ".bai"])


def test_compress_cram(cram_tmp_path, bam_tmp_file, cram_api, cram_tmp_index_path):
    """Test decompress a real cram file"""
    # GIVEN a existing bam file
    assert bam_tmp_file.exists()
    # GIVEN a non existing cram path
    assert not cram_tmp_path.exists()
    # GIVEN a non existing cram index path
    cram_tmp_index_path = pathlib.Path(cram_tmp_index_path)
    assert not cram_tmp_index_path.exists()
    # GIVEN a cram api

    # WHEN decompressing the cram file
    res = cram_api.compress(bam_path=str(bam_tmp_file), cram_path=str(cram_tmp_path))

    # THEN assert that the process executed with success
    assert res is True
    # THEN assert that the cram file was created
    assert cram_tmp_path.exists()
    # THEN assert that the cram index file was created
    assert cram_tmp_index_path.exists()
