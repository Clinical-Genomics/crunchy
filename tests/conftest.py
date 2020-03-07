"""Base conftest file"""
import logging
import pathlib

import pytest

from crunchy.command import SpringProcess

LOG = logging.getLogger(__name__)


class MockSpringProcess(SpringProcess):
    """Mock the Spring API"""

    def __init__(self, binary="spring", threads=8, tmp_dir=None):
        """docstring for __init__"""
        super().__init__(binary, threads, tmp_dir)
        self.compress_success = None
        self.decompress_success = None

    def run_command(self, parameters=None):
        """Mock out the run command functionality"""
        LOG.info("Running command %s", " ".join(parameters))
        if self.compress_success is True:
            self.stdout = "Compression done!\ntotal time for compression: 4 s\n"
        if self.decompress_success is True:
            self.stdout = "Decompression done!\ntotal time for decompression: 4 s\n"
        return True


@pytest.fixture
def first_read():
    """Return the path first read in read pair"""
    _file_path = pathlib.Path(
        "tests/fixtures/fastqs/CPCT12345678R_HJJLGCCXX_S1_L001_R1_001.fastq.gz"
    )
    return _file_path


@pytest.fixture
def second_read():
    """Return the path second read in read pair"""
    _file_path = pathlib.Path(
        "tests/fixtures/fastqs/CPCT12345678R_HJJLGCCXX_S1_L001_R2_001.fastq.gz"
    )
    return _file_path


@pytest.fixture
def spring_path():
    """Return the path to a spring compressed file"""
    _file_path = pathlib.Path(
        "tests/fixtures/spring/CPCT12345678R_HJJLGCCXX_S1_L001.spring"
    )
    return _file_path


@pytest.fixture
def spring_api():
    """Return a mocked spring api"""
    return MockSpringProcess("spring", threads=8)


@pytest.fixture
def fixtures_dir():
    """Return the path to a dummy file"""
    _dir_path = pathlib.Path("tests/fixtures")
    return _dir_path


@pytest.fixture
def dummy_file_path():
    """Return the path to a dummy file"""
    _file_path = pathlib.Path("tests/fixtures/dummy.txt")
    return _file_path


@pytest.fixture
def zipped_file_path():
    """Return the path to a zipped dummy file"""
    _file_path = pathlib.Path("tests/fixtures/zipped_file.txt.gz")
    return _file_path
