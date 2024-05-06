"""Fixtures to test the command module"""

import pytest


@pytest.fixture
def spring_api(real_spring_api):
    """Return a spring api that runs spring"""
    return real_spring_api


@pytest.fixture
def cram_api(real_cram_api):
    """Return a cram api"""
    return real_cram_api
