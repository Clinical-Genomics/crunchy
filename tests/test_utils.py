"""Tests for utils"""
from crunchy.fastq import spring_outpath
from crunchy.utils import find_fastq_pairs


def test_find_fastq_pairs_fixtures(fixtures_dir, first_read, second_read):
    """Test to find all fastq pairs in a directory"""
    # GIVEN the path to a directory with fastq files
    assert fixtures_dir.is_dir()
    spring_path = spring_outpath(first_read)
    # WHEN finding all fastq pairs
    pairs = find_fastq_pairs(fixtures_dir)
    res = next(pairs)
    # THEN assert that the correct reads are retuned
    assert res[0] == first_read
    assert res[1] == second_read
    assert res[2] == spring_path
