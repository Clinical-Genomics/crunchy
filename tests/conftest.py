"""Base conftest file"""
import copy
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


class MockCramProcess:
    """Mock the Spring API"""

    def __init__(self, binary="samtools", refgenome_path="genome.fasta", threads=8):
        """Initialize a CramProcessMock"""
        self.binary = binary
        self.refgenome_path = refgenome_path
        self.threads = threads
        self.base_call = [self.binary]
        self.stdout = ""
        self.stderr = ""

    def run_command(self, parameters=None):
        """Execute a command in the shell

        Args:
            parameters(list)
        """
        command = copy.deepcopy(self.base_call)
        if parameters:
            command.extend(parameters)

        LOG.info("Running command %s", " ".join(command))

        return 0

    def decompress(self, cram_path: str, bam_path: str) -> bool:
        """Convert cram to bam"""
        LOG.info("Decompressing cram %s to bam %s", cram_path, bam_path)
        parameters = [
            "view",
            "-b",
            "-o",
            bam_path,
            "-r",
            self.refgenome_path,
            cram_path,
        ]
        return self.run_command(parameters)

    def compress(self, parameters=None):
        """Mock out the run compress functionality"""
        LOG.info("Running command %s", " ".join(parameters))
        return self.run_command(parameters)

    def index(self, file_path: str):
        """Index a bam or cram file"""
        LOG.info("Creating index for %s", file_path)
        index_type = ".cram"
        if file_path.endswith(".bam"):
            index_type = ".bai"
        parameters = ["index", file_path, ".".join([file_path, index_type])]
        return self.run_command(parameters)


@pytest.fixture(name="fixtures_dir")
def fixture_fixtures_dir():
    """Return the path to a the fixtures dir"""
    _dir_path = pathlib.Path("tests/fixtures")
    return _dir_path


@pytest.fixture
def dummy_file_path(fixtures_dir):
    """Return the path to a dummy file"""
    _file_path = fixtures_dir / "dummy.txt"
    return _file_path


@pytest.fixture
def zipped_file_path(fixtures_dir):
    """Return the path to a zipped dummy file"""
    _file_path = fixtures_dir / "zipped_file.txt.gz"
    return _file_path


@pytest.fixture(name="bam_path")
def fixture_bam_path(fixtures_dir):
    """Return the path to a bam file"""
    _file_path = fixtures_dir / "bam" / "test.bam"
    return _file_path


@pytest.fixture(name="cram_path")
def fixture_cram_path(fixtures_dir):
    """Return the path to a cram file"""
    _file_path = fixtures_dir / "bam" / "test.cram"
    return _file_path


@pytest.fixture
def first_read(fixtures_dir):
    """Return the path first read in read pair"""
    _file_path = (
        fixtures_dir / "fastq" / "CPCT12345678R_HJJLGCCXX_S1_L001_R1_001.fastq.gz"
    )
    return _file_path


@pytest.fixture
def second_read(fixtures_dir):
    """Return the path second read in read pair"""
    _file_path = (
        fixtures_dir / "fastq" / "CPCT12345678R_HJJLGCCXX_S1_L001_R2_001.fastq.gz"
    )
    return _file_path


@pytest.fixture(name="spring_path")
def fixture_spring_path(fixtures_dir):
    """Return the path to a spring compressed file"""
    _file_path = fixtures_dir / "spring" / "CPCT12345678R_HJJLGCCXX_S1_L001.spring"
    return _file_path


@pytest.fixture
def spring_api():
    """Return a mocked spring api"""
    return MockSpringProcess("spring", threads=8)


@pytest.fixture
def cram_api():
    """Return a mocked spring api"""
    return MockSpringProcess("spring", threads=8)
