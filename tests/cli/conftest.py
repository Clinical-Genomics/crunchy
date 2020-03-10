"""Fixtures for CLI tests"""
import pathlib
import tempfile

import pytest


@pytest.fixture(scope="function", name="base_context")
def fixture_base_context(spring_api, cram_api) -> dict:
    """context to use in cli"""

    return {
        "spring_api": spring_api,
        "cram_api": cram_api,
    }


@pytest.yield_fixture
def non_existing_path() -> pathlib.Path:
    """Return the path tp a non existing file"""
    _file_path = pathlib.Path(tempfile.NamedTemporaryFile().name)
    yield _file_path
