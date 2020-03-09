"""Utilities for crunchy cli functions"""
import logging
import pathlib

import click

LOG = logging.getLogger(__name__)


def file_exists(file_path: pathlib.Path) -> bool:
    """Check if a file exists.

    If not raise a click.Abort("File <file_path> does not exist")
    """
    if not file_path.exists():
        LOG.error("Could not find file %s", file_path)
        raise click.Abort
    return True
