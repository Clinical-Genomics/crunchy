"""
crunchy.__main__
~~~~~~~~~~~~~~~~~~~~~

The main entry point for the command line interface.

Invoke as ``crunchy`` (if installed)
or ``python -m crunchy`` (no install required).
"""
import sys

from crunchy.cli.base import base_command

if __name__ == "__main__":
    # exit using whatever exit code the CLI returned
    sys.exit(base_command())
