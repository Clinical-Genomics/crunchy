"""Code to test the CLI compress commands"""

import logging
import pathlib

from click.testing import CliRunner

from crunchy.cli.compress_cmd import bam, compress, fastq

LOG = logging.getLogger(__name__)


def test_compress_cmd():
    """Test to run the compress base command"""
    # GIVEN a cli runner
    runner = CliRunner()
    # WHEN running the compress command with dry_run
    result = runner.invoke(compress, obj={})
    # THEN assert the command was succesful even without a valid api
    assert result.exit_code == 0


def test_compress_bam_dry_run(bam_tmp_file, base_context):
    """Test to run the compress bam command"""
    # GIVEN the path to a existing bam file and a cli runner
    runner = CliRunner()
    bam_path = bam_tmp_file
    assert bam_path.exists()
    # WHEN running the compress command with dry_run
    result = runner.invoke(bam, ["--bam-path", str(bam_path), "--dry-run"], obj=base_context)
    # THEN assert the command was succesful
    assert result.exit_code == 0


def test_compress_bam_no_outpath(base_context, bam_tmp_file):
    """Test to run the compress bam command"""
    # GIVEN the path to a bam file and a cli runner
    runner = CliRunner()
    bam_path = bam_tmp_file
    assert bam_path.exists()
    # WHEN running the compress command
    result = runner.invoke(
        bam,
        ["--bam-path", bam_path],
        obj=base_context,
    )
    # THEN assert the command was succesful
    assert result.exit_code == 0


def test_compress_bam_valid_outpath(base_context, bam_path):
    """Test to run the compress bam command"""
    # GIVEN the path to a bam file, a non existing outpath and a cli runner
    outpath = "a_file.cram"
    runner = CliRunner()
    # WHEN running the compress command
    result = runner.invoke(
        bam,
        ["--bam-path", str(bam_path), "--cram-path", outpath],
        obj=base_context,
    )
    # THEN assert the command was succesful
    assert result.exit_code == 0


def test_compress_bam_existing_outpath(base_context, bam_path, cram_path):
    """Test to run the compress bam command"""
    # GIVEN the path to a bam file, a existing outpath and a cli runner
    runner = CliRunner()
    assert cram_path.exists()
    # WHEN running the compress command
    res = runner.invoke(
        bam,
        ["--bam-path", str(bam_path), "--cram-path", str(cram_path)],
        obj=base_context,
    )
    # THEN the progam should abort since the cram file already exists
    assert res.exit_code == 1


def test_compress_fastq_dry_run(first_read, second_read):
    """Test to run the compress fastq command"""
    # GIVEN the path to a existing bam file and a cli runner
    runner = CliRunner()
    assert first_read.exists()
    assert second_read.exists()
    # WHEN running the compress command with dry_run
    result = runner.invoke(
        fastq,
        [
            "--first-read",
            str(first_read),
            "--second-read",
            str(second_read),
            "--dry-run",
        ],
        obj={},
    )
    # THEN assert the command was succesful even without a valid api
    assert result.exit_code == 0


def test_compress_fastq_dry_run_integrity(first_read, second_read):
    """Test to run the compress fastq with integrity check in dry run mode"""
    # GIVEN the path to a existing bam file and a cli runner
    runner = CliRunner()
    assert first_read.exists()
    assert second_read.exists()
    # WHEN running the compress command with dry_run
    result = runner.invoke(
        fastq,
        [
            "--first-read",
            str(first_read),
            "--second-read",
            str(second_read),
            "--dry-run",
            "--check-integrity",
        ],
        obj={},
    )
    # THEN assert the command was succesful even without a valid api
    assert result.exit_code == 0


def test_compress_fastq_existing_spring_file(first_read, second_read, spring_path, base_context):
    """Test to run the compress fastq command"""
    # GIVEN the path to a existing bam file and a cli runner
    runner = CliRunner()
    assert spring_path.exists()
    # WHEN running the compress command with dry_run
    result = runner.invoke(
        fastq,
        [
            "--first-read",
            str(first_read),
            "--second-read",
            str(second_read),
            "--spring-path",
            str(spring_path),
        ],
        obj=base_context,
    )
    # THEN assert the command failed since the spring file exists
    assert result.exit_code == 1


def test_compress_fastq_valid_spring_file(first_read, second_read, spring_tmp_path, base_context):
    """Test to run the compress fastq command"""
    # GIVEN the path to a existing bam file and a cli runner
    runner = CliRunner()
    assert not spring_tmp_path.exists()
    # WHEN running the compress command with dry_run
    result = runner.invoke(
        fastq,
        [
            "--first-read",
            str(first_read),
            "--second-read",
            str(second_read),
            "--spring-path",
            str(spring_tmp_path),
        ],
        obj=base_context,
    )
    # THEN assert the command succedes
    assert result.exit_code == 0


def test_compress_fastq_with_metadata(
    first_read, second_read, spring_tmp_path, base_context, metadata_tmp_path
):
    """Test to run the compress fastq command with metadata written"""
    # GIVEN the path a pair of fastqs, a spring file and a cli runner
    runner = CliRunner()
    # GIVEN a non existing spring path
    assert not spring_tmp_path.exists()
    # GIVEN a non existing metadata path
    assert not metadata_tmp_path.exists()
    # WHEN running the compress command with metadata
    result = runner.invoke(
        fastq,
        [
            "--first-read",
            str(first_read),
            "--second-read",
            str(second_read),
            "--spring-path",
            str(spring_tmp_path),
            "--metadata-file",
        ],
        obj=base_context,
    )
    # THEN assert the command succedes
    assert result.exit_code == 0
    # THEN assert the metadata file was created
    assert metadata_tmp_path.exists()


def nr_files(dirpath: pathlib.Path) -> int:
    """Count the number of files in a directory"""
    nr_files_indir = 0
    for path in dirpath.iterdir():
        if not path.is_file():
            continue
        nr_files_indir += 1
    return nr_files_indir
