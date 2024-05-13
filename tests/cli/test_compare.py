"""Tests for compare CLI"""

from click.testing import CliRunner

from crunchy.cli.base import base_command
from crunchy.integrity import get_checksum


def test_compare_same(first_read):
    """Test to compare a file with itself"""
    # GIVEN the path to a gzipped file and a cli runner
    runner = CliRunner()
    # WHEN running the compare command
    result = runner.invoke(base_command, ["compare", "-f", str(first_read), "-s", str(first_read)])
    # THEN assert the command was succesful
    assert result.exit_code == 0


def test_compare_checksum(first_read):
    """Test to compare a file with a checksum"""
    # GIVEN the path to a gzipped file, a checksum and a cli runner
    checksum = get_checksum(first_read)
    runner = CliRunner()
    # WHEN running the compare command
    result = runner.invoke(base_command, ["compare", "-f", str(first_read), "-c", checksum])
    # THEN assert the command was succesful
    assert result.exit_code == 0


def test_compare_checksum_two_reads(first_read):
    """Test to compare two files AND a checksum"""
    # GIVEN the path to a gzipped file, a checksum and a cli runner
    checksum = get_checksum(first_read)
    runner = CliRunner()
    # WHEN running the compare command with both files and a checksum
    result = runner.invoke(
        base_command,
        ["compare", "-f", str(first_read), "-s", str(first_read), "-c", checksum],
    )
    # THEN assert the command fails since two files can not be compared to one checksum
    assert result.exit_code == 1


def test_compare_wrong_checksum(first_read, second_read):
    """Test to compare a file with a wrong checksum"""
    # GIVEN the path to a gzipped file and a cli runner
    runner = CliRunner()
    # GIVEN a mismatching checksum
    checksum = get_checksum(second_read)
    # WHEN running the compare command with one file and the wrong checksum
    result = runner.invoke(
        base_command,
        ["compare", "-f", str(first_read), "-c", checksum],
    )
    # THEN assert the command fails checksums differ
    assert result.exit_code == 1


def test_compare_different(first_read, second_read):
    """Test to compare two different files"""
    # GIVEN the path to a gzipped file and a cli runner
    runner = CliRunner()
    # WHEN running the compare command
    result = runner.invoke(base_command, ["compare", "-f", str(first_read), "-s", str(second_read)])
    # THEN assert the command was succesful
    assert result.exit_code == 1


def test_check_logging(first_read):
    """Test to compare a file with itself"""
    # GIVEN the path to a gzipped file and a cli runner
    runner = CliRunner()
    # GIVEN a checksum for the read
    checksum = get_checksum(first_read)
    # WHEN running the compare command
    result = runner.invoke(base_command, ["compare", "-f", str(first_read), "-s", str(first_read)])
    # THEN assert the checksum that is logged is the same
    new_checksum = None
    for message in result.output.split("\n"):
        if "Checksum:" in message:
            new_checksum = message.split(" ")[-1]

    assert checksum == new_checksum
