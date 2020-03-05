"""Base conftest file"""
import logging
import pathlib

import pytest

from crunchy.command import SpringProcess

LOG = logging.getLogger(__name__)


class MockSpringProcess(SpringProcess):
    def run_command(self, parameters=None):
        """Mock out the run command functionality"""
        LOG.info("Running command %s", " ".join(command))
        return 0


@pytest.fixture
def dummy_file_path():
    """Return the path to a dummy file"""
    _file_path = pathlib.Path("tests/fixtures/dummy.txt")
    return _file_path


@pytest.fixture
def zipped_file_path():
    """Return the path to a zipped dummy file"""
    _file_path = pathlib.Path("tests/fixtures/zipped_file.txt.gz")
    return _file_path


@pytest.fixture
def spring_api():
    """Return a mocked spring api"""
    return MockSpringProcess("spring", threads=8)
