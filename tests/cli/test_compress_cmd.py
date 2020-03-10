"""Code to test the CLI compress commands"""
from click.testing import CliRunner

from crunchy.cli.compress_cmd import cram, spring


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
