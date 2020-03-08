"""CLI functionality for crunchy"""
import logging
import pathlib

import click
import coloredlogs

from .command import SpringProcess
from .compress import compress as compress_function
from .decompress import decompress as decompress_function
from .fastq import fastq_outpaths
from .integrity import compare_elements, get_checksum
from .utils import find_fastq_pairs

LOG = logging.getLogger(__name__)
LOG_LEVELS = ["DEBUG", "INFO", "WARNING"]


def file_exists(file_path: pathlib.Path) -> bool:
    """Check if a file exists.

    If not raise a click.Abort("File <file_path> does not exist")
    """
    if not file_path.exists():
        LOG.error("Could not find file %s", file_path)
        raise click.Abort
    return True


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


@click.command()
@click.option(
    "--first",
    "-f",
    type=click.Path(exists=True),
    required=True,
    help="First read in pair",
)
@click.option(
    "--second",
    "-s",
    type=click.Path(exists=True),
    required=True,
    help="Second read in pair",
)
@click.option(
    "--spring-path",
    "-o",
    type=click.Path(exists=False),
    required=True,
    help="Path to spring file",
)
@click.option("--dry-run", is_flag=True)
@click.pass_context
def compress(ctx, first, second, spring_path, dry_run):
    """Compress a pair of fastq files with spring"""
    LOG.info("Running compress")
    spring_api = ctx.obj.get("spring_api")
    first = pathlib.Path(first)
    second = pathlib.Path(second)
    outfile = pathlib.Path(spring_path)
    try:
        compress_function(
            first=first,
            second=second,
            outfile=outfile,
            spring_api=spring_api,
            dry_run=dry_run,
        )
    except SyntaxError as err:
        LOG.error(err)
        raise click.Abort


@click.command()
@click.argument("spring-path", type=click.Path(exists=True))
@click.option(
    "--first", "-f", type=click.Path(exists=False), help="First read in pair",
)
@click.option(
    "--second", "-s", type=click.Path(exists=False), help="Second read in pair",
)
@click.option(
    "--dry-run", is_flag=True, help="Skip deleting original files",
)
@click.pass_context
def decompress(ctx, spring_path, first, second, dry_run):
    """Decompress a file"""
    LOG.info("Running decompress")
    spring_api = ctx.obj.get("spring_api")
    spring_path = pathlib.Path(spring_path)
    try:
        file_exists(spring_path)
    except click.Abort as err:
        if dry_run:
            LOG.warning("Dry run! Continue")
        else:
            raise err

    if not (first or second):
        LOG.warning("No filenames provided. Guess outfiles")
        fastqs = fastq_outpaths(spring_path)
        first = fastqs[0]
        second = fastqs[1]

    first = pathlib.Path(first)
    second = pathlib.Path(second)
    if first.exists() or second.exists():
        LOG.error("Outpath(s) already exists! Specify new with '-f', '-s'")
        raise click.Abort()

    decompress_function(
        spring_path=spring_path,
        first=first,
        second=second,
        spring_api=spring_api,
        dry_run=dry_run,
    )


@click.command()
@click.argument("infile", type=click.Path(exists=True), nargs=-1)
@click.option(
    "--algorithm", "-a", type=click.Choice(["md5", "sha1", "sha256"]), default="sha256"
)
@click.option("--compare", "-c", is_flag=True)
def checksum(infile, algorithm, compare):
    """Create a checksum for the file(s) raise syntax error if two files differ."""
    LOG.info("Running checksum")
    checksums = []
    for _infile in infile:
        _infile = pathlib.Path(_infile)
        file_exists(_infile)
        checksums.append(get_checksum(_infile, algorithm))

    if compare:
        if not compare_elements(checksums):
            LOG.warning("All checksums are NOT the same")
            raise click.Abort
        LOG.info("All checksums are the same")

    for _checksum in checksums:
        click.echo(_checksum)


@click.command()
@click.argument("spring-path", type=click.Path(exists=True))
@click.option(
    "--first",
    "-f",
    type=click.Path(exists=True),
    help="First in fastq pair to compare",
)
@click.option(
    "--second",
    "-s",
    type=click.Path(exists=True),
    help="Second in fastq pair to compare",
)
@click.option(
    "--dry-run", is_flag=True, help="Skip deleting original files",
)
@click.pass_context
def delete(ctx, spring_path, first, second, dry_run):
    """Decompress a spring file and compare to original files. If they are identical keep only the
    spring file"""
    LOG.info("Running delete")

    if not first:
        LOG.info("No fastq paths provided. Guess based on spring name")
        first, second = fastq_outpaths(pathlib.Path(spring_path))
    else:
        first = pathlib.Path(first)
    file_exists(first)
    file_exists(second)

    first_spring = pathlib.Path(first).with_suffix(".spring.fastq")
    second_spring = pathlib.Path(second).with_suffix(".spring.fastq")
    ctx.invoke(
        decompress,
        spring_path=spring_path,
        first=str(first_spring),
        second=str(second_spring),
        dry_run=dry_run,
    )

    success = True
    try:
        ctx.invoke(checksum, str(first), str(first_spring), compare=True)
        ctx.invoke(checksum, str(second), str(second_spring), compare=True)
    except click.Abort:
        LOG.error("Uncompressed spring differ from original fastqs")
        success = False

    if success:
        LOG.info("Files are identical")
        LOG.info("Removing original fastqs")
        if not dry_run:
            first.unlink()
            LOG.info("%s deleted", first)
            second.unlink()
            LOG.info("%s deleted", second)

    LOG.info("Deleting decompressed spring files")
    first_spring.unlink()
    LOG.info("%s deleted", first_spring)
    second_spring.unlink()
    LOG.info("%s deleted", second_spring)


@click.command()
@click.option("--indir", type=click.Path(exists=True))
@click.option("--dry-run", is_flag=True)
@click.option("--spring-path", type=click.Path(exists=False))
@click.option(
    "--first",
    "-f",
    type=click.Path(exists=True),
    help="First in fastq pair to compare",
)
@click.option(
    "--second",
    "-s",
    type=click.Path(exists=True),
    help="Second in fastq pair to compare",
)
@click.pass_context
def auto(ctx, indir, spring_path, first, second, dry_run):
    """Run whole pipeline by compressing, comparing and deleting original fastqs.
    Either all fastq pairs below a directory or a given pair.
    """
    if indir:
        LOG.info(
            "Running auto, this will recursively compress and delete fastqs in %s",
            indir,
        )
        indir = pathlib.Path(indir)
        if not indir.is_dir():
            LOG.warning("Please specify a directory")
            return
        pairs = find_fastq_pairs(indir)

    else:
        if not (first and second and spring_path):
            LOG.warning(
                "Please specify either a directory or two fastqs and a spring path"
            )
            return
        LOG.info(
            "Running auto, this will recursively compress and delete fastqs %s, %s",
            first,
            second,
        )

        pairs = [(pathlib.Path(first), pathlib.Path(second), pathlib.Path(spring_path))]

    for pair in pairs:
        first_fastq = str(pair[0])
        second_fastq = str(pair[1])
        spring_path = str(pair[2])
        try:
            ctx.invoke(
                compress,
                first=first_fastq,
                second=second_fastq,
                spring_path=spring_path,
                dry_run=dry_run,
            )
            ctx.invoke(
                delete,
                spring_path=spring_path,
                first=first,
                second=second,
                dry_run=dry_run,
            )
        except click.Abort:
            LOG.warning("Skip current and continue auto")
            continue


base_command.add_command(checksum)
base_command.add_command(decompress)
base_command.add_command(compress)
base_command.add_command(delete)
base_command.add_command(auto)
