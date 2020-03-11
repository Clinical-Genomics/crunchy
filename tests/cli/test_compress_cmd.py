"""Code to test the CLI compress commands"""
import logging
import pathlib

from click.testing import CliRunner

from crunchy.cli import compare_cmd
from crunchy.cli.compress_cmd import compress, cram, spring

LOG = logging.getLogger(__name__)


def test_compress_cmd():
    """Test to run the compress base command"""
    # GIVEN a cli runner
    runner = CliRunner()
    # WHEN running the compress command with dry_run
    result = runner.invoke(compress, obj={})
    # THEN assert the command was succesful even without a valid api
    assert result.exit_code == 0


def test_compress_cram_dry_run(bam_tmp_file):
    """Test to run the compress cram command"""
    # GIVEN the path to a existing bam file and a cli runner
    runner = CliRunner()
    bam_path = bam_tmp_file
    assert bam_path.exists()
    # WHEN running the compress command with dry_run
    result = runner.invoke(cram, ["--bam-path", str(bam_path), "--dry-run"], obj={})
    # THEN assert the command was succesful even without a valid api
    assert result.exit_code == 0


def test_compress_cram_no_outpath(base_context, bam_tmp_file):
    """Test to run the compress cram command"""
    # GIVEN the path to a bam file and a cli runner
    runner = CliRunner()
    bam_path = bam_tmp_file
    assert bam_path.exists()
    # WHEN running the compress command
    result = runner.invoke(cram, ["--bam-path", bam_path], obj=base_context,)
    # THEN assert the command was succesful
    assert result.exit_code == 0


def test_compress_cram_valid_outpath(base_context, bam_path):
    """Test to run the compress cram command"""
    # GIVEN the path to a bam file, a non existing outpath and a cli runner
    outpath = "a_file.cram"
    runner = CliRunner()
    # WHEN running the compress command
    result = runner.invoke(
        cram, ["--bam-path", bam_path, "--cram-path", outpath], obj=base_context,
    )
    # THEN assert the command was succesful
    assert result.exit_code == 0


def test_compress_cram_existing_outpath(base_context, bam_path, cram_path):
    """Test to run the compress cram command"""
    # GIVEN the path to a bam file, a existing outpath and a cli runner
    runner = CliRunner()
    assert cram_path.exists()
    # WHEN running the compress command
    res = runner.invoke(
        cram, ["--bam-path", bam_path, "--cram-path", cram_path], obj=base_context,
    )
    # THEN the progam should abort since file already exists
    assert res.exit_code == 1


def test_compress_spring_dry_run(first_read, second_read):
    """Test to run the compress spring command"""
    # GIVEN the path to a existing bam file and a cli runner
    runner = CliRunner()
    assert first_read.exists()
    assert second_read.exists()
    # WHEN running the compress command with dry_run
    result = runner.invoke(
        spring,
        ["--first", str(first_read), "--second", str(second_read), "--dry-run"],
        obj={},
    )
    # THEN assert the command was succesful even without a valid api
    assert result.exit_code == 0


def test_compress_spring_existing_spring_file(
    first_read, second_read, spring_path, base_context
):
    """Test to run the compress spring command"""
    # GIVEN the path to a existing bam file and a cli runner
    runner = CliRunner()
    assert spring_path.exists()
    # WHEN running the compress command with dry_run
    result = runner.invoke(
        spring,
        [
            "--first",
            str(first_read),
            "--second",
            str(second_read),
            "--spring-path",
            str(spring_path),
        ],
        obj=base_context,
    )
    # THEN assert the command failed since the spring file exists
    assert result.exit_code == 1


def test_compress_spring_valid_spring_file(
    first_read, second_read, spring_tmp_path, base_context
):
    """Test to run the compress spring command"""
    # GIVEN the path to a existing bam file and a cli runner
    runner = CliRunner()
    assert not spring_tmp_path.exists()
    # WHEN running the compress command with dry_run
    result = runner.invoke(
        spring,
        [
            "--first",
            str(first_read),
            "--second",
            str(second_read),
            "--spring-path",
            str(spring_tmp_path),
        ],
        obj=base_context,
    )
    # THEN assert the command succedes
    assert result.exit_code == 0


def test_compress_spring_real(
    first_read, second_read, spring_tmp_path, real_base_context
):
    """Test to run the compress spring command"""
    # GIVEN the path to a existing bam file and a cli runner
    runner = CliRunner()
    assert not spring_tmp_path.exists()
    # WHEN running the compress command with dry_run
    result = runner.invoke(
        spring,
        [
            "--first",
            str(first_read),
            "--second",
            str(second_read),
            "--spring-path",
            str(spring_tmp_path),
        ],
        obj=real_base_context,
    )
    # THEN assert the command succedes
    assert result.exit_code == 0
    # THEN assert that the spring file was created
    assert spring_tmp_path.exists()


def nr_files(dirpath: pathlib.Path) -> int:
    """Count the number of files in a directory"""
    nr_files_indir = 0
    for path in dirpath.iterdir():
        if not path.is_file():
            continue
        nr_files_indir += 1
    return nr_files_indir


def test_compress_spring_real_with_integrity(
    first_tmp_file, second_tmp_file, spring_tmp_path, real_base_context
):
    """Test to run the compress spring command with integrity check"""
    # GIVEN the path to a existing two existing fastq files and a non existing spring
    runner = CliRunner()
    assert not spring_tmp_path.exists()
    assert first_tmp_file.exists()
    assert second_tmp_file.exists()

    dir_path = spring_tmp_path.parent
    assert nr_files(dir_path) == 2
    # WHEN running the compress command with an intergrity check
    result = runner.invoke(
        spring,
        [
            "--first",
            str(first_tmp_file),
            "--second",
            str(second_tmp_file),
            "--spring-path",
            str(spring_tmp_path),
            "--check-integrity",
        ],
        obj=real_base_context,
    )
    # THEN assert the command succedes
    assert result.exit_code == 0
    # THEN assert that the spring file was created
    assert spring_tmp_path.exists()
    # THEN assert that the files created for integrity check was removed
    assert nr_files(dir_path) == 3


def test_compress_spring_real_with_integrity_fail(
    first_tmp_file, second_tmp_file, spring_tmp_path, real_base_context, mocker
):
    """Test to run the compress spring command when integrity check fails"""
    # GIVEN the path to a existing two existing fastq files and a non existing spring
    runner = CliRunner()
    assert not spring_tmp_path.exists()
    assert first_tmp_file.exists()
    assert second_tmp_file.exists()

    dir_path = spring_tmp_path.parent
    assert nr_files(dir_path) == 2
    mocker.patch.object(compare_cmd, "compare_elements")
    compare_cmd.compare_elements.return_value = False
    # WHEN running the compress command with an intergrity check
    result = runner.invoke(
        spring,
        [
            "--first",
            str(first_tmp_file),
            "--second",
            str(second_tmp_file),
            "--spring-path",
            str(spring_tmp_path),
            "--check-integrity",
        ],
        obj=real_base_context,
    )
    # THEN assert the command succedes
    print(result.__dict__)
    assert result.exit_code == 1
    # THEN assert that the spring file was deleted
    assert not spring_tmp_path.exists()
    # THEN assert that only the original fastq files are left
    assert nr_files(dir_path) == 2
