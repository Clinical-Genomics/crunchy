"""Test for the auto functionality in crunchy"""

import pathlib

from click.testing import CliRunner

from crunchy.cli.auto_cmd import auto, fastq


def nr_files(dirpath: pathlib.Path) -> int:
    """Count the number of files in a directory"""
    nr_files_indir = 0
    for path in dirpath.iterdir():
        if not path.is_file():
            continue
        nr_files_indir += 1
    return nr_files_indir


def test_auto_base():
    """Test base command"""
    # GIVEN a cli runner
    runner = CliRunner()
    # WHEN running the auto base command
    result = runner.invoke(auto)
    # THEN assert it exits without problems
    assert result.exit_code == 0


def test_auto_pairs(base_context, first_tmp_file, second_tmp_file):
    """Test auto fastq with files"""
    # GIVEN a cli runner
    runner = CliRunner()
    # WHEN running the auto base command
    result = runner.invoke(
        fastq, ["-f", first_tmp_file, "-s", second_tmp_file, "--yes"], obj=base_context
    )
    # THEN assert it exits without problems
    assert result.exit_code == 0


def test_auto_pairs_and_spring(base_context, first_tmp_file, second_tmp_file, spring_tmp_path):
    """Test auto fastq with files"""
    # GIVEN a cli runner
    runner = CliRunner()
    # WHEN running the auto base command
    result = runner.invoke(
        fastq, ["-f", first_tmp_file, "-s", second_tmp_file, "--yes"], obj=base_context
    )
    # THEN assert it exits without problems
    assert result.exit_code == 0


def test_auto_dir_dry_run(base_context, project_dir):
    """Test auto fastq with dir"""
    # GIVEN a cli runner
    runner = CliRunner()
    # WHEN running the auto base command
    result = runner.invoke(
        fastq, ["--indir", str(project_dir), "--yes", "--dry-run"], obj=base_context
    )
    # THEN assert it exits without problems
    assert result.exit_code == 0


def test_auto_dir_nodir_dry_run(base_context, first_read):
    """Test auto fastq when dir is no dir"""
    # GIVEN a cli runner
    runner = CliRunner()
    # WHEN running the auto base command
    result = runner.invoke(
        fastq, ["--indir", str(first_read), "--yes", "--dry-run"], obj=base_context
    )
    # THEN assert it exits without running
    assert result.exit_code == 0
