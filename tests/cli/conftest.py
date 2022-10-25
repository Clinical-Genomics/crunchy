"""Fixtures for CLI tests"""
import tempfile
from pathlib import Path
from typing import Any, Generator

import pytest

from crunchy.command import SpringProcess, CramProcess
from tests.conftest import MockSpringProcess, MockCramProcess


@pytest.fixture(name="base_context")
def fixture_base_context(spring_api: MockSpringProcess, cram_api: MockCramProcess) -> dict[str, Any]:
    """Return base context to use in CLI."""
    return {
        "spring_api": spring_api,
        "cram_api": cram_api,
    }


@pytest.fixture(name="real_base_context")
def fixture_real_base_context(real_spring_api: SpringProcess, real_cram_api: CramProcess) -> dict[str, Any]:
    """Return real base context to use in CLI."""
    return {
        "spring_api": real_spring_api,
        "cram_api": real_cram_api,
    }


@pytest.fixture(name="non_existing_path")
def fixture_non_existing_path() -> Generator[Path, None, None]:
    """Return the path tp a non-existing file."""
    yield Path(tempfile.NamedTemporaryFile().name)
