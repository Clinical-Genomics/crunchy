"""Utilities for crunchy cli functions"""
import logging
import pathlib

import click

LOG = logging.getLogger(__name__)


def file_exists(file_path: pathlib.Path, exists: bool = True) -> bool:
    """Check if a file exists.

    If not raise a click.Abort("File <file_path> does not exist")
    If make sure that file does not exist set exists to False
    """
    if file_path.exists():
        if exists is False:
            LOG.error("File %s already exists!", file_path)
            raise click.Abort
    else:
        if exists is True:
            LOG.error("Could not find file %s", file_path)
            raise click.Abort

    return True
