"""Base conftest file"""
import logging
import pathlib
import shutil
import sys

import pytest

from crunchy.command import CramProcess, SpringProcess

LOG = logging.getLogger(__name__)
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)


@pytest.fixture(name="fixtures_dir")
def fixture_fixtures_dir():
    """Return the path to a the fixtures dir"""
    _dir_path = pathlib.Path("tests/fixtures")
    return _dir_path


# File paths fixtures #


@pytest.fixture(name="reference_path")
def fixture_reference_path(fixtures_dir):
    """Return the path to fasta reference"""
    _file_path = fixtures_dir / "chr_m.fasta"
    return _file_path


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


@pytest.fixture(name="first_read")
def fixture_first_read(fixtures_dir):
    """Return the path first read in read pair"""
    _file_path = (
        fixtures_dir / "fastq" / "CPCT12345678R_HJJLGCCXX_S1_L001_R1_001.fastq.gz"
    )
    return _file_path


@pytest.fixture(name="second_read")
def fixture_second_read(fixtures_dir):
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


# Temp files fixtures #


@pytest.fixture(scope="function", name="project_dir")
def fixture_project_dir(tmpdir_factory):
    """Path to a temporary directory"""
    my_tmpdir = pathlib.Path(tmpdir_factory.mktemp("data"))
    yield my_tmpdir
    shutil.rmtree(str(my_tmpdir))


# Paths to non existing files #


@pytest.fixture(name="first_tmp_path")
def fixture_first_tmp_path(first_read, project_dir):
    """Return the path to a nonexisting fastq file"""
    _file_path = project_dir / first_read.name
    return _file_path


@pytest.fixture(name="second_tmp_path")
def fixture_second_tmp_path(second_read, project_dir):
    """Return the path to a nonexisting fastq file"""
    _file_path = project_dir / second_read.name
    return _file_path


@pytest.fixture(name="spring_tmp_path")
def fixture_spring_tmp_path(spring_path, project_dir):
    """Return the path to a nonexisting temporary spring file"""
    _spring_tmp = project_dir / spring_path.name
    return _spring_tmp


@pytest.fixture(name="bam_tmp_path")
def fixture_bam_tmp_path(bam_path, project_dir):
    """Return the path to a nonexisting small bam file"""
    _file_path = project_dir / bam_path.name
    return _file_path


@pytest.fixture(name="cram_tmp_path")
def fixture_cram_tmp_path(cram_path, project_dir):
    """Return the path to a nonexisting temporary cram file"""
    _file_path = project_dir / cram_path.name
    return _file_path


@pytest.fixture(name="cram_tmp_index_path")
def fixture_cram_tmp_index_path(cram_tmp_path, real_cram_api):
    """Return the path to a nonexisting temporary cram file"""
    _index_path = real_cram_api.get_index_path(cram_tmp_path)
    return _index_path


# Paths to existing temporary files #


@pytest.fixture(name="first_tmp_file")
def fixture_first_tmp_file(first_tmp_path, first_read):
    """Return the path to a temporary fastq file"""
    shutil.copy(str(first_read), str(first_tmp_path))
    return first_tmp_path


@pytest.fixture(name="second_tmp_file")
def fixture_second_tmp_file(second_tmp_path, second_read):
    """Return the path to a temporary fastq file"""
    shutil.copy(str(second_read), str(second_tmp_path))
    return second_tmp_path


@pytest.fixture(name="spring_tmp_file")
def fixture_spring_tmp_file(spring_tmp_path, spring_path):
    """Return the path to a temporary spring file"""
    shutil.copy(str(spring_path), str(spring_tmp_path))
    return spring_tmp_path


@pytest.fixture
def bam_tmp_file(bam_path, bam_tmp_path):
    """Return the path to a temporary small bam file"""
    shutil.copy(str(bam_path), str(bam_tmp_path))
    return bam_tmp_path


@pytest.fixture
def cram_tmp_file(cram_path, cram_tmp_path):
    """Return the path to a temporary cram file"""
    shutil.copy(str(cram_path), str(cram_tmp_path))
    return cram_tmp_path


# Fixtures for apis #


@pytest.fixture(name="spring_api")
def fixture_spring_api():
    """Return a mocked spring api"""
    return MockSpringProcess("spring", threads=8)


@pytest.fixture(name="cram_api")
def fixture_cram_api():
    """Return a mocked spring api"""
    return MockCramProcess("samtools", threads=8)


@pytest.fixture(name="real_spring_api")
def fixture_real_spring_api():
    """Return a spring api that runs spring"""
    return SpringProcess("spring", threads=8)


@pytest.fixture(name="real_cram_api")
def fixture_real_cram_api(reference_path):
    """Return a cram api"""
    return CramProcess("samtools", refgenome_path=str(reference_path))


class MockSpringProcess:
    """Mock the Spring API"""

    def __init__(self, binary="spring", threads=8, tmp_dir=None):
        """docstring for __init__"""
        self.binary = binary
        self.threads = threads
        self.base_call = [self.binary]
        self.tmp = tmp_dir or "./tmp"

    @staticmethod
    def run_command(parameters=None):
        """Mock out the run command functionality"""
        LOG.info("Running command %s", " ".join(parameters))
        return 0

    def decompress(
        self, spring_path: pathlib.Path, first: pathlib.Path, second: pathlib.Path
    ) -> bool:
        """Run the spring decompress command"""
        parameters = ["-d", "-i", str(spring_path), "-o", str(first), str(second)]
        self.run_command(parameters)
        return True

    def compress(
        self, first: pathlib.Path, second: pathlib.Path, outfile: pathlib.Path
    ) -> bool:
        """Run the spring compression command"""
        parameters = [
            "-c",
            "-i",
            str(first),
            str(second),
            "-o",
            str(outfile),
            "-t",
            str(self.threads),
        ]
        self.run_command(parameters)
        return True


class MockCramProcess:
    """Mock the Spring API"""

    def __init__(self, binary="samtools", refgenome_path="genome.fasta", threads=8):
        """Initialize a CramProcessMock"""
        self.binary = binary
        self.refgenome_path = refgenome_path
        self.threads = threads
        self.base_call = [self.binary]

    @staticmethod
    def run_command(parameters=None):
        """Execute a command in the shell

        Args:
            parameters(list)
        """
        LOG.info("Running command %s", " ".join(parameters))
        return 0

    def decompress(self, cram_path: pathlib.Path, bam_path: pathlib.Path) -> bool:
        """Convert cram to bam"""
        LOG.info("Decompressing cram %s to bam %s", cram_path, bam_path)
        parameters = [
            "view",
            "-b",
            "-o",
            str(bam_path),
            "-r",
            self.refgenome_path,
            str(cram_path),
        ]
        self.run_command(parameters)
        return True

    def compress(self, bam_path: pathlib.Path, cram_path: pathlib.Path) -> bool:
        """Convert bam to cram"""
        LOG.info("Compressing bam %s to cram %s", bam_path, cram_path)
        parameters = [
            "view",
            "-C",
            "-T",
            self.refgenome_path,
            str(bam_path),
            "-o",
            str(cram_path),
        ]
        self.run_command(parameters)
        self.index(cram_path)
        return True

    def index(self, file_path: pathlib.Path):
        """Index a bam or cram file"""
        LOG.info("Creating index for %s", file_path)
        index_type = ".cram"
        if file_path.suffix == ".bam":
            index_type = ".bai"
        index_path = file_path.with_suffix(file_path.suffix + index_type)
        parameters = ["index", str(file_path), str(index_path)]
        self.run_command(parameters)
        return True
