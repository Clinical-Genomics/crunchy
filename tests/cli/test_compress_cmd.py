"""Code to test the CLI compress commands"""

from click.testing import CliRunner

from crunchy.cli.base import base_command


def test_compress_cram(base_context, bam_path):
    """Test to run the compress cram command"""
    # GIVEN the path to a gzipped file and a cli runner
    runner = CliRunner()
    # WHEN running the compare command
    result = runner.invoke(
        base_command, ["compress", "cram", "--bam-path", bam_path], obj=base_context
    )
    # THEN assert the command was succesful
    assert result.exit_code == 0
