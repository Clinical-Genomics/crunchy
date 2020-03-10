"""Tests for compare CLI"""

from click.testing import CliRunner

from crunchy.cli.base import base_command


def test_compare_same(first_read):
    """Test to compare a file with itself"""
    # GIVEN the path to a gzipped file and a cli runner
    runner = CliRunner()
    # WHEN running the compare command
    result = runner.invoke(
        base_command, ["compare", "-f", str(first_read), "-s", str(first_read)]
    )
    # THEN assert the command was succesful
    assert result.exit_code == 0


def test_compare_different(first_read, second_read):
    """Test to compare two different files"""
    # GIVEN the path to a gzipped file and a cli runner
    runner = CliRunner()
    # WHEN running the compare command
    result = runner.invoke(
        base_command, ["compare", "-f", str(first_read), "-s", str(second_read)]
    )
    # THEN assert the command was succesful
    assert result.exit_code == 1
