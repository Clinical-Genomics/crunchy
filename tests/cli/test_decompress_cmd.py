"""Tests for decompress command"""
import pathlib
import shutil
from pathlib import Path

from click.testing import CliRunner

from crunchy.cli.decompress_cmd import cram, decompress, spring
from crunchy.files import fastq_outpaths
from crunchy.integrity import get_checksum


def nr_files(dirpath: pathlib.Path) -> int:
    """Count the number of files in a directory"""
    nr_files_indir = 0
    for path in dirpath.iterdir():
        if not path.is_file():
            continue
        nr_files_indir += 1
    return nr_files_indir


def test_decompress_cram(base_context, cram_tmp_file, bam_tmp_path):
    """Test to run the decompress cram command"""
    # GIVEN a cli runner
    runner = CliRunner()
    # WHEN running the decompress cram command
    result = runner.invoke(
        cram, [str(cram_tmp_file), "-b", str(bam_tmp_path)], obj=base_context
    )
    # THEN assert the command succeeds
    assert result.exit_code == 0


def test_decompress_cmd():
    """Test to run the decompress base command"""
    # GIVEN a cli runner
    runner = CliRunner()
    # WHEN running the compress command with dry_run
    result = runner.invoke(decompress, obj={})
    # THEN assert the command was succesful even without a valid api
    assert result.exit_code == 0


def test_decompress_spring_non_existing_spring(base_context, spring_tmp_path):
    """Test to run decompress spring with a non existing spring file"""
    # GIVEN a cli runner
    runner = CliRunner()
    # GIVEN non existing spring file
    assert not spring_tmp_path.exists()
    # WHEN running the de compress command with non existing spring file
    result = runner.invoke(spring, [str(spring_tmp_path)], obj=base_context)
    # THEN assert the command fails since the spring file needs to exist
    assert result.exit_code == 2


def test_decompress_spring_no_fastq(spring_tmp_file, base_context):
    """Test to run decompress spring command without specifying the out paths"""
    # GIVEN a cli runner
    runner = CliRunner()
    # GIVEN two non existing fastq paths
    fastq1, fastq2 = fastq_outpaths(spring_tmp_file)
    assert not (fastq1.exists() or fastq2.exists())
    # WHEN running the decompress command without fastq files
    result = runner.invoke(spring, [str(spring_tmp_file)], obj=base_context)
    # THEN assert the command was succesful since crunchy creates the file names
    assert result.exit_code == 0


def test_decompress_spring_no_fastq_existing_paths(
    spring_tmp_file, first_read, second_read, base_context
):
    """Test to run the compress base command"""
    # GIVEN a cli runner and the path to an existing spring file
    runner = CliRunner()
    # GIVEN two existing fastq files
    fastqs = fastq_outpaths(spring_tmp_file)
    first = fastqs[0]
    second = fastqs[1]
    shutil.copy(str(first_read), str(first))
    shutil.copy(str(second_read), str(second))
    assert first.exists()
    # WHEN running the decompress command without fastq files
    result = runner.invoke(spring, [str(spring_tmp_file)], obj=base_context)
    # THEN assert the command fails since the autogenerated fastq files exists
    assert result.exit_code == 1


def test_decompress_spring_with_fastq(
    spring_tmp_file, first_tmp_path, second_tmp_path: Path, base_context
):
    """Test to run the compress base command"""
    # GIVEN a cli runner
    runner = CliRunner()
    # WHEN running the decompress command with fastq files
    result = runner.invoke(
        spring,
        [str(spring_tmp_file), "-f", str(first_tmp_path), "-s", second_tmp_path.as_posix()],
        obj=base_context,
    )
    # THEN assert the command was succesful
    assert result.exit_code == 0


def test_decompress_spring_with_result(
    spring_tmp_file,
    first_tmp_path,
    second_tmp_path: Path,
    base_context,
    first_read,
    second_read,
):
    """Test to run decompress spring command where the mock creates output files"""
    # GIVEN a cli runner
    runner = CliRunner()
    # GIVEN fasq paths that does not exist
    assert not (first_tmp_path.exists() or second_tmp_path.exists())
    # GIVEN a mock that produces output
    base_context["spring_api"]._create_output = True
    base_context["spring_api"]._fastq1 = first_read
    base_context["spring_api"]._fastq2 = second_read
    # WHEN running the decompress command with fastq files
    result = runner.invoke(
        spring,
        [str(spring_tmp_file), "-f", str(first_tmp_path), "-s", second_tmp_path.as_posix()],
        obj=base_context,
    )
    # THEN assert the command was succesful
    assert result.exit_code == 0
    # THEN assert that the fastq files where created by the mock
    assert first_tmp_path.exists() and second_tmp_path.exists()


def test_decompress_spring_with_fastq_and_integrity_check(
    spring_tmp_file,
    first_tmp_path,
    second_tmp_path: Path,
    base_context,
    first_read,
    second_read,
):
    """Test to run decompress spring command with integrity check."""
    # GIVEN a cli runner
    runner = CliRunner()
    # GIVEN fasq paths that does not exist
    assert not (first_tmp_path.exists() or second_tmp_path.exists())
    # GIVEN a mock that produces output
    base_context["spring_api"]._create_output = True
    base_context["spring_api"]._fastq1 = first_read
    base_context["spring_api"]._fastq2 = second_read
    # GIVEN checksums for the original fastq files
    checksum1 = get_checksum(first_read)
    checksum2 = get_checksum(second_read)
    # WHEN running the decompress command with fastq files
    result = runner.invoke(
        spring,
        [
            str(spring_tmp_file),
            "-f",
            str(first_tmp_path),
            "-s",
            second_tmp_path.as_posix(),
            "--first-checksum",
            checksum1,
            "--second-checksum",
            checksum2,
        ],
        obj=base_context,
    )
    # THEN assert the command was succesful
    assert result.exit_code == 0
    # THEN assert that the integrity check was successful
    assert first_tmp_path.exists() and second_tmp_path.exists()


def test_decompress_spring_with_fastq_failing_integrity_check(
    spring_tmp_file,
    first_tmp_path,
    second_tmp_path: Path,
    base_context,
    first_read,
    second_read,
):
    """Test to run decompress spring command with a failing integrity check"""
    # GIVEN a cli runner
    runner = CliRunner()
    # GIVEN fasq paths that does not exist
    assert not (first_tmp_path.exists() or second_tmp_path.exists())
    # GIVEN a mock that produces output
    base_context["spring_api"]._create_output = True
    base_context["spring_api"]._fastq1 = first_read
    base_context["spring_api"]._fastq2 = second_read
    # GIVEN checksums for the original fastq files
    checksum1 = get_checksum(first_read)
    # GIVEN wrong checksum for second read
    checksum2 = get_checksum(first_read)
    # WHEN running the decompress command with fastq files
    result = runner.invoke(
        spring,
        [
            str(spring_tmp_file),
            "-f",
            str(first_tmp_path),
            "-s",
            second_tmp_path.as_posix(),
            "--first-checksum",
            checksum1,
            "--second-checksum",
            checksum2,
        ],
        obj=base_context,
    )
    # THEN assert the command was succesful
    assert result.exit_code == 1
    # THEN assert that the fastq files are deleted since check failed
    assert not (first_tmp_path.exists() or second_tmp_path.exists())


def test_decompress_spring_with_fastq_real_run(
    spring_tmp_file, first_tmp_path, second_tmp_path: Path, real_base_context
):
    """Test to run the decompress spring command"""
    # GIVEN a cli runner
    runner = CliRunner()
    dir_path = spring_tmp_file.parent
    # GIVEN a directory with one spring file
    assert nr_files(dir_path) == 1
    # WHEN running the decompress command with real data
    result = runner.invoke(
        spring,
        [str(spring_tmp_file), "-f", str(first_tmp_path), "-s", second_tmp_path.as_posix()],
        obj=real_base_context,
    )
    # THEN assert the command was succesful
    assert result.exit_code == 0
    # THEN assert that the fastq files are created
    assert nr_files(dir_path) == 3
    assert first_tmp_path.exists()
    assert second_tmp_path.exists()
