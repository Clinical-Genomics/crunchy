"""Test for the auto functionality in crunchy"""
import pathlib

from click.testing import CliRunner

from crunchy.cli.auto_cmd import auto, fastq
from crunchy.files import spring_outpath


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


def test_auto_pairs_and_spring(
    base_context, first_tmp_file, second_tmp_file, spring_tmp_path
):
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


def test_auto_dir_real_data(
    real_base_context, first_tmp_file, second_tmp_file, project_dir
):
    """Test auto fastq with dir"""
    # GIVEN a cli runner and a path to a directory with a pair of fastq files
    runner = CliRunner()
    assert nr_files(project_dir) == 2
    assert first_tmp_file.exists()
    assert second_tmp_file.exists()
    spring_path = spring_outpath(first_tmp_file)
    assert not spring_path.exists()
    # WHEN running the auto base command
    result = runner.invoke(
        fastq, ["--indir", str(project_dir), "--yes"], obj=real_base_context
    )
    # THEN assert it exits without problems
    assert result.exit_code == 0
    # THEN assert that the spring file was created
    assert spring_path.exists()
    # THEN assert that the original fastq files was deleted
    assert not first_tmp_file.exists()
    assert not second_tmp_file.exists()
    # THEN assert that no intermediate files are left
    assert nr_files(project_dir) == 1
