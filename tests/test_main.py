"""Test the __main__ module"""

import subprocess


def test_main():
    """Test to run the test module"""
    completed = subprocess.run(["python", "-m", "crunchy"])
    assert completed.returncode == 0
