"""CLI functionality for crunchy"""
import logging

import click
import coloredlogs

from crunchy.command import SpringProcess

from .auto_cmd import auto
from .compare_cmd import compare
from .compress_cmd import compress
from .decompress_cmd import decompress

LOG = logging.getLogger(__name__)
LOG_LEVELS = ["DEBUG", "INFO", "WARNING"]


@click.group()
@click.option(
    "--spring-binary", default="spring", show_default=True, help="Path to spring binary"
)
@click.option(
    "--threads",
    "-t",
    default=8,
    show_default=True,
    help="Number of threads to use for spring compression",
)
@click.option(
    "--log-level",
    default="INFO",
    type=click.Choice(LOG_LEVELS),
    help="Choose what log messages to show",
)
@click.option(
    "--tmp-dir", help="If specific temp dir should be used",
)
@click.pass_context
def base_command(ctx, spring_binary, threads, log_level, tmp_dir):
    """Base command for crunchy"""
    coloredlogs.install(level=log_level)
    spring_api = SpringProcess(spring_binary, threads, tmp_dir)
    ctx.obj = {"spring_api": spring_api}
    LOG.info("Running crunchy")


base_command.add_command(compare)
base_command.add_command(decompress)
base_command.add_command(compress)
base_command.add_command(auto)
