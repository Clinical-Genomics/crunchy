"""Fixtures to test the command module"""
import logging
import pathlib
import shutil

import pytest

from crunchy.command import CramProcess, SpringProcess

LOG = logging.getLogger(__name__)


@pytest.fixture(name="cram_tmp_path")
def fixture_cram_tmp_path(cram_path, tmp_path):
    """Return the path to a nonexisting temporary cram file"""
    _file_path = tmp_path / cram_path.name
    return _file_path


@pytest.fixture(name="cram_tmp_index_path")
def fixture_cram_tmp_index_path(cram_tmp_path, cram_api):
    """Return the path to a nonexisting temporary cram file"""
    _index_path = cram_api.get_index_path(cram_tmp_path)
    return _index_path


@pytest.fixture
def cram_tmp_file(cram_path, cram_tmp_path):
    """Return the path to a temporary cram file"""
    shutil.copy(str(cram_path), str(cram_tmp_path))
    return cram_tmp_path


@pytest.fixture(name="spring_tmp_path")
def fixture_spring_tmp_path(spring_path, tmp_path):
    """Return the path to a nonexisting temporary spring file"""
    _spring_tmp = tmp_path / spring_path.name
    return _spring_tmp


@pytest.fixture(name="spring_tmp_file")
def fixture_spring_tmp_file(spring_tmp_path, spring_path):
    """Return the path to a temporary spring file"""
    shutil.copy(str(spring_path), str(spring_tmp_path))
    return spring_tmp_path


@pytest.fixture(name="first_tmp_path")
def fixture_first_tmp_path(first_read, tmp_path):
    """Return the path to a nonexisting fastq file"""
    _file_path = tmp_path / first_read.name
    return _file_path


@pytest.fixture(name="first_tmp_file")
def fixture_first_tmp_file(first_tmp_path, first_read):
    """Return the path to a temporary fastq file"""
    shutil.copy(str(first_read), str(first_tmp_path))
    return first_tmp_path


@pytest.fixture(name="second_tmp_path")
def fixture_second_tmp_path(second_read, tmp_path):
    """Return the path to a nonexisting fastq file"""
    _file_path = tmp_path / second_read.name
    return _file_path


@pytest.fixture(name="second_tmp_file")
def fixture_second_tmp_file(second_tmp_path, second_read):
    """Return the path to a temporary fastq file"""
    shutil.copy(str(second_read), str(second_tmp_path))
    return second_tmp_path


@pytest.fixture
def spring_api():
    """Return a spring api that runs spring"""
    return SpringProcess("spring", threads=8)


@pytest.fixture
def cram_api(reference_path):
    """Return a cram api"""
    return CramProcess("samtools", refgenome_path=str(reference_path))


@pytest.fixture(name="reference_path")
def fixture_reference_path():
    """Return the path to fasta reference"""
    _file_path = pathlib.Path("tests/fixtures/chr_m.fasta")
    return _file_path
