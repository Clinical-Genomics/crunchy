"""Base conftest file."""
import logging
from pathlib import Path
import shutil
import sys
from typing import Generator

import pytest

from crunchy.command import CramProcess, SpringProcess
from crunchy.integrity import get_checksum

LOG = logging.getLogger(__name__)
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)


@pytest.fixture(name="fixtures_dir")
def fixture_fixtures_dir() -> Path:
    """Return the path to the fixture's dir."""
    return Path("tests/fixtures")


# File paths fixtures #


@pytest.fixture(name="reference_path")
def fixture_reference_path(fixtures_dir: Path) -> Path:
    """Return the path to FASTA reference."""
    return Path(fixtures_dir, "reference.fasta")


@pytest.fixture
def dummy_file_path(fixtures_dir: Path) -> Path:
    """Return the path to a dummy file."""
    return Path(fixtures_dir, "dummy.txt")


@pytest.fixture
def zipped_file_path(fixtures_dir: Path) -> Path:
    """Return the path to a zipped dummy file."""
    return Path(fixtures_dir, "zipped_file.txt.gz")


@pytest.fixture(name="bam_path")
def fixture_bam_path(fixtures_dir: Path) -> Path:
    """Return the path to a BAM file."""
    return Path(fixtures_dir, "bam", "test.bam")


@pytest.fixture(name="cram_path")
def fixture_cram_path(fixtures_dir: Path) -> Path:
    """Return the path to a CRAN file"""
    return Path(fixtures_dir, "bam", "test.cram")


@pytest.fixture(name="first_read")
def fixture_first_read(fixtures_dir: Path) -> Path:
    """Return the path first read in read pair."""
    return Path(fixtures_dir, "fastq", "TEST_R1_001.fq.gz")


@pytest.fixture(name="second_read")
def fixture_second_read(fixtures_dir: Path) -> Path:
    """Return the path second read in read pair."""
    return Path(fixtures_dir, "fastq", "TEST_R2_001.fq.gz")


@pytest.fixture(name="spring_path")
def fixture_spring_path(fixtures_dir: Path) -> Path:
    """Return the path to a Spring compressed file."""
    return Path(fixtures_dir, "spring", "TEST.spring")


# Temp files fixtures #


@pytest.fixture(scope="function", name="project_dir")
def fixture_project_dir(tmpdir_factory) -> Generator[Path, None, None]:
    """Path to a temporary directory."""
    yield Path(tmpdir_factory.mktemp("data"))


# Paths to non existing files #


@pytest.fixture(name="first_tmp_path")
def fixture_first_tmp_path(project_dir: Path, first_read: Path) -> Path:
    """Return the path to a nonexistent FASTQ file."""
    return Path(project_dir, first_read.name)


@pytest.fixture(name="second_tmp_path")
def fixture_second_tmp_path(project_dir: Path, second_read: Path) -> Path:
    """Return the path to a nonexistent FASTQ file."""
    return Path(project_dir, second_read.name)


@pytest.fixture(name="spring_tmp_path")
def fixture_spring_tmp_path(project_dir: Path, spring_path: Path) -> Path:
    """Return the path to a nonexistent temporary Spring file."""
    return Path(project_dir, spring_path.name)


@pytest.fixture(name="bam_tmp_path")
def fixture_bam_tmp_path(bam_path: Path, project_dir: Path) -> Path:
    """Return the path to a nonexistent small BAM file."""
    return Path(project_dir, bam_path.name)


@pytest.fixture(name="cram_tmp_path")
def fixture_cram_tmp_path(cram_path: Path, project_dir: Path) -> Path:
    """Return the path to a nonexistent temporary CRAM file."""
    return Path(project_dir, cram_path.name)


@pytest.fixture(name="cram_tmp_index_path")
def fixture_cram_tmp_index_path(cram_tmp_path: Path, real_cram_api: CramProcess) -> Path:
    """Return the path to a nonexistent temporary CRAM file."""
    return real_cram_api.get_index_path(cram_tmp_path)


@pytest.fixture(name="metadata_tmp_path")
def fixture_metadata_tmp_path(spring_tmp_path: Path) -> Path:
    """Return the path to a nonexisting temporary spring metadata file."""
    return spring_tmp_path.with_suffix(".json")


# Paths to existing temporary files #


@pytest.fixture(name="first_tmp_file")
def fixture_first_tmp_file(first_tmp_path: Path, first_read: Path) -> Path:
    """Return the path to a temporary FASTQ file."""
    shutil.copy(first_read.as_posix(), first_tmp_path.as_posix())
    return first_tmp_path


@pytest.fixture(name="second_tmp_file")
def fixture_second_tmp_file(second_tmp_path: Path, second_read: Path) -> Path:
    """Return the path to a temporary FASTQ file."""
    shutil.copy(second_read.as_posix(), second_tmp_path.as_posix())
    return second_tmp_path


@pytest.fixture(name="spring_tmp_file")
def fixture_spring_tmp_file(spring_tmp_path: Path, spring_path: Path) -> Path:
    """Return the path to a temporary Spring file."""
    shutil.copy(spring_path.as_posix(), spring_tmp_path.as_posix())
    return spring_tmp_path


@pytest.fixture
def bam_tmp_file(bam_path: Path, bam_tmp_path: Path) -> Path:
    """Return the path to a temporary small bam file"""
    shutil.copy(bam_path.as_posix(), bam_tmp_path.as_posix())
    return bam_tmp_path


@pytest.fixture
def cram_tmp_file(cram_path: Path, cram_tmp_path: Path) -> Path:
    """Return the path to a temporary CRAM file."""
    shutil.copy(cram_path.as_posix(), cram_tmp_path.as_posix())
    return cram_tmp_path


# Fixtures for checksums #


@pytest.fixture(name="checksum_first_read")
def fixture_checksum_first_read(first_read: Path) -> str:
    """Return the checksum for first FASTQ read."""
    return get_checksum(first_read)


@pytest.fixture(name="checksum_second_read")
def fixture_checksum_second_read(second_read: Path) -> str:
    """Return the checksum for second FASTQ read."""
    return get_checksum(second_read)


# Fixtures for metadata


@pytest.fixture(name="spring_metadata")
def fixture_spring_metadata(
    first_read: Path, second_read: Path, spring_tmp_path: Path, checksum_first_read: str, checksum_second_read: str
):
    """Return metadata information."""
    return [{"path": str(first_read.absolute()), "file": "first_read", "checksum": checksum_first_read, "algorithm": "sha256",}, {"path": str(second_read.absolute()), "file": "second_read", "checksum": checksum_second_read, "algorithm": "sha256",}, {"path": str(spring_tmp_path.absolute()), "file": "spring"},]



class MockSpringProcess:
    """Mock the Spring API."""

    def __init__(self, binary="spring", threads=8, tmp_dir=None):
        """Initialize a MockSpringProcess."""
        self.binary = binary
        self.threads = threads
        self.base_call = [self.binary]
        self.tmp = tmp_dir or "./tmp"
        self._create_output = False
        self._fastq1 = None
        self._fastq2 = None

    @staticmethod
    def run_command(parameters=None):
        """Mock out the run command functionality."""
        LOG.info("Running command %s", " ".join(parameters))
        return 0

    def decompress(
        self, spring_path: Path, first: Path, second: Path
    ) -> bool:
        """Run the spring decompress command."""
        parameters = ["-d", "-i", spring_path.as_posix(), "-o", first.as_posix(), second.as_posix()]
        self.run_command(parameters)
        if self._create_output:
            LOG.info(f"Create output fastq files {self._fastq1} and {self._fastq2}")
            shutil.copy(str(self._fastq1), first.as_posix())
            shutil.copy(str(self._fastq2), second.as_posix())
        return True

    def compress(
        self, first: Path, second: Path, outfile: Path
    ) -> bool:
        """Run the spring compression command."""
        parameters = [
            "-c",
            "-i",
            first.as_posix(),
            second.as_posix(),
            "-o",
            outfile.as_posix(),
            "-t",
            str(self.threads),
        ]
        self.run_command(parameters)
        return True


class MockCramProcess:
    """Mock the CRAM API."""

    def __init__(self, binary="samtools", refgenome_path="genome.fasta", threads=8):
        """Initialize a CramProcessMock."""
        self.binary = binary
        self.refgenome_path = refgenome_path
        self.threads = threads
        self.base_call = [self.binary]

    @staticmethod
    def run_command(parameters=None) -> int:
        """Execute a command in the shell.

        Args:
            parameters(list)
        """
        LOG.info("Running command %s", " ".join(parameters))
        return 0

    def decompress(self, cram_path: Path, bam_path: Path) -> bool:
        """Convert CRAM to BAM."""
        LOG.info("Decompressing cram %s to bam %s", cram_path, bam_path)
        parameters = [
            "view",
            "-b",
            "-o",
            bam_path.as_posix(),
            "-r",
            self.refgenome_path,
            cram_path.as_posix(),
        ]
        self.run_command(parameters)
        return True

    def compress(self, bam_path: Path, cram_path: Path) -> bool:
        """Convert BAM to CRAM."""
        LOG.info(f"Compressing bam {bam_path} to cram {cram_path}")
        parameters = [
            "view",
            "-C",
            "-T",
            self.refgenome_path,
            bam_path.as_posix(),
            "-o",
            cram_path.as_posix(),
        ]
        self.run_command(parameters)
        self.index(cram_path)
        return True

    def index(self, file_path: Path) -> bool:
        """Index a BAN or CRAM file."""
        LOG.info("Creating index for %s", file_path)
        index_type: str = ".bai" if file_path.suffix == ".bam" else ".cram"
        index_path: Path = file_path.with_suffix(file_path.suffix + index_type)
        parameters: list[str] = ["index", file_path.as_posix(), index_path.as_posix()]
        self.run_command(parameters)
        return True

    @staticmethod
    def self_check():
        """Mocks the self test."""
        return True


# Fixtures for apis #


@pytest.fixture(name="spring_api")
def fixture_spring_api() -> MockSpringProcess:
    """Return a mocked Spring API."""
    return MockSpringProcess("spring", threads=8)


@pytest.fixture(name="cram_api")
def fixture_cram_api() -> MockCramProcess:
    """Return a mocked Spring API."""
    return MockCramProcess("samtools", threads=8)


@pytest.fixture(name="real_spring_api")
def fixture_real_spring_api() -> SpringProcess:
    """Return a Spring API that runs Spring"""
    return SpringProcess("spring", threads=8)


@pytest.fixture(name="real_cram_api")
def fixture_real_cram_api(reference_path: Path) -> CramProcess:
    """Return a CRAM API."""
    return CramProcess("samtools", refgenome_path=str(reference_path))
