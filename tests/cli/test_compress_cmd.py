"""Code to test the CLI compress commands"""
from click.testing import CliRunner

from crunchy.cli.compress_cmd import cram


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
