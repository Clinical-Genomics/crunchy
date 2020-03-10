"""Fixtures for CLI tests"""
import pytest


@pytest.fixture(scope="function", name="base_context")
def fixture_base_context(spring_api, cram_api) -> dict:
    """context to use in cli"""

    return {
        "spring_api": spring_api,
        "cram_api": cram_api,
    }
