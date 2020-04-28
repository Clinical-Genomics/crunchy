"""CLI functionality for crunchy"""
import logging

import click
import coloredlogs

from crunchy.command import CramProcess, SpringProcess
from crunchy.version import __version__

from .auto_cmd import auto
from .checksum_cmd import checksum
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
    "--samtools-binary",
    default="samtools",
    show_default=True,
    help="Path to spring binary",
)
@click.option(
    "--threads",
    "-t",
    default=8,
    show_default=True,
    help="Number of threads to use for spring compression",
)
@click.version_option(__version__)
@click.option(
    "--reference", "-r", help="Path to reference genome",
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
def base_command(
    ctx, spring_binary, samtools_binary, threads, reference, log_level, tmp_dir
):
    """Base command for crunchy

    \b
                  .---. .---.
                 :     : o   :    me want cookie!
             _..-:   o :     :-.._    /
         .-''  '  `---' `---' "   ``-.
       .'   "   '  "  .    "  . '  "  `.
      :   '.---.,,.,...,.,.,.,..---.  ' ;
      `. " `.                     .' " .'
       `.  '`.                   .' ' .'
        `.    `-._           _.-' "  .'  .----.
          `. "    '"--...--"'  . ' .'  .'  o   `.
          .'`-._'    " .     " _.-'`. :       o  :
        .'      ```--.....--'''    ' `:_ o       :
      .'    "     '         "     "   ; `.;";";";'
     ;         '       "       '     . ; .' ; ; ;
    ;     '         '       '   "    .'      .-'
    '  "     "   '      "           "    _.-'
    """
    coloredlogs.install(level=log_level)
    spring_api = SpringProcess(spring_binary, threads, tmp_dir)
    ctx.obj = {}
    ctx.obj["spring_api"] = spring_api
    cram_api = CramProcess(samtools_binary, reference, threads)
    ctx.obj["cram_api"] = cram_api
    LOG.info("Running crunchy")


base_command.add_command(compare)
base_command.add_command(decompress)
base_command.add_command(compress)
base_command.add_command(auto)
base_command.add_command(checksum)
