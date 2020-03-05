"""CLI functionality for crunchy"""
import logging
import pathlib

import click
import coloredlogs

from .command import SpringProcess
from .compress import compress as compress_function
from .decompress import decompress as decompress_function
from .integrity import compare_elements, get_checksum
from .utils import compress_and_delete

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
@click.pass_context
def base_command(ctx, spring_binary, threads, log_level):
    """Base command for crunchy"""
    coloredlogs.install(level=log_level)
    spring_api = SpringProcess(spring_binary, threads)
    ctx.obj = {"spring_api": spring_api}
    LOG.info("Running crunchy")


@click.command()
@click.argument("infile", type=click.Path(exists=True), nargs=-1)
@click.option(
    "--algorithm", "-a", type=click.Choice(["md5", "sha1", "sha256"]), default="sha256"
)
@click.option("--compare", "-c", is_flag=True)
def checksum(infile, algorithm, compare):
    """Create a checksum for the file(s)"""
    LOG.info("Running checksum")
    checksums = []
    for _infile in infile:
        checksums.append(get_checksum(pathlib.Path(_infile), algorithm))
    if compare:
        if compare_elements(checksums):
            LOG.info("All checksums are the same")
        else:
            LOG.warning("All checksums are NOT the same")
    for _checksum in checksums:
        click.echo(_checksum)


@click.command()
@click.argument("infile", type=click.Path(exists=True))
@click.option("--outfile", "-o", type=click.Path(exists=False))
@click.option(
    "--second",
    "-s",
    type=click.Path(exists=True),
    help="If there are paired fastqs to unpack",
)
@click.pass_context
def decompress(ctx, infile, outfile, second):
    """Decompress a file"""
    LOG.info("Running decompress")
    spring_api = ctx.obj.get("spring_api")
    infile = pathlib.Path(infile)
    if second:
        second = pathlib.Path(second)
    try:
        decompress_function(
            filepath=infile, second=second, outfile=outfile, spring_api=spring_api
        )
    except SyntaxError:
        return


@click.command()
@click.argument("infile", type=click.Path(exists=True))
@click.option("--compression", type=click.Choice(["gzip", "spring"]), default="spring")
@click.option(
    "--second", "-s", type=click.Path(exists=True), help="If there are paired fastqs"
)
@click.option("--outfile", "-o", type=click.Path(exists=False))
@click.pass_context
def compress(ctx, infile, compression, second, outfile):
    """Compress a file"""
    LOG.info("Running compress to format %s", compression)
    infile = pathlib.Path(infile)
    spring_api = None
    if compression == "spring":
        spring_api = ctx.obj.get("spring_api")
    if second:
        second = pathlib.Path(second)
    if outfile:
        outfile = pathlib.Path(outfile)
    try:
        compress_function(
            filepath=infile, second=second, outfile=outfile, spring_api=spring_api,
        )
    except SyntaxError:
        return


@click.command()
@click.argument("indir", type=click.Path(exists=True))
@click.option("--dry-run", is_flag=True)
@click.pass_context
def auto(ctx, indir, dry_run):
    """Recursively find all fastq pairs below a directory and spring compress them.
    Uncompress, check it they are identical and finally remove original fastq files
    """
    LOG.info(
        "Running auto, this will recursively compress and delete all fastqs in given dir"
    )
    indir = pathlib.Path(indir)
    spring_api = ctx.obj["spring_api"]

    if not indir.is_dir():
        LOG.warning("Please specify a directory")
        return

    compress_and_delete(indir, spring_api)


base_command.add_command(checksum)
base_command.add_command(decompress)
base_command.add_command(compress)
base_command.add_command(auto)
