"""
Code to handle communications to the shell.
"""

import copy
import logging
import subprocess
from pathlib import Path
from subprocess import CalledProcessError
from typing import Optional, List, Generator

LOG = logging.getLogger(__name__)


class Process:
    """Class to handle communication with other programs via the shell.

    The other parts of the code should not need to have any knowledge about how the processes are
    called, that will be handled in this module.Output form stdout and stdin will be handeld here.
    """

    def __init__(self, binary: str, config: Optional[str] = None, config_parameter: str = "--config"):
        """
        Args:
            binary(str): Path to binary for the process to use
            config(str): Path to config if used by process
        """
        super(Process, self).__init__()
        self.binary: str = binary
        LOG.info(f"Initialising Process with binary: {self.binary}")
        self.base_call: List[str] = [self.binary]
        if config:
            self.base_call.extend([config_parameter, config])
        LOG.info(f"Use base call {self.base_call}")
        self._stdout: str = ""
        self._stderr: str = ""

    def run_command(self, parameters=None):
        """Execute a command in the shell.

        Args:
            parameters(list)
        """
        command = copy.deepcopy(self.base_call)
        if parameters:
            command.extend(parameters)

        LOG.info("Running command %s", " ".join(command))
        res = subprocess.run(
            command, check=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )

        self.stdout = res.stdout.decode("utf-8").rstrip()
        self.stderr = res.stderr.decode("utf-8").rstrip()
        if res.returncode != 0:
            LOG.critical(f"Call {command} exit with a non zero exit code", )
            LOG.critical(self.stderr)
            raise CalledProcessError(command, res.returncode)

        return res.returncode

    @property
    def stdout(self):
        """Fetch stdout."""
        return self._stdout

    @stdout.setter
    def stdout(self, text):
        self._stdout = text

    @stdout.deleter
    def stdout(self):
        del self._stdout

    @property
    def stderr(self):
        """Fetch stderr."""
        return self._stderr

    @stderr.setter
    def stderr(self, text):
        self._stderr = text

    @stderr.deleter
    def stderr(self):
        del self._stderr

    def stdout_lines(self) -> Generator[List[str], None, None]:
        """Iterate over the lines in self.stdout."""
        yield from self.stdout.split("\n")

    def stderr_lines(self) -> Generator[List[str], None, None]:
        """Iterate over the lines in self.stderr."""
        yield from self.stderr.split("\n")

    def __repr__(self) -> str:
        return f"Process:base_call:{self.base_call}"


class SpringProcess(Process):
    """Process to deal with String commands."""

    def __init__(self, binary: str, threads: int = 8, tmp_dir: Optional[str] = None):
        """Initialise a spring process."""
        super().__init__(binary)
        self.threads: int = threads
        self.tmp: Optional[str] = tmp_dir

    def decompress(
        self, spring_path: Path, first: Path, second: Path
    ) -> bool:
        """Run the spring decompress command."""
        parameters = ["-d", "-i", str(spring_path), "-o", str(first), str(second)]
        if first.suffix == ".gz":
            LOG.info("Compressing to gzipped format")
            parameters.append("-g")

        if self.tmp:
            parameters.extend(["--working-dir", self.tmp])

        LOG.info("Decompressing Spring compressed file")
        self.run_command(parameters)
        success = False
        time_to_decompress = "unknown"
        for line in self.stdout_lines():
            line = line.lower()
            if "decompression done" in line:
                success = True
            if "total time for decompression" in line:
                time_to_decompress = line.split(" ")[-2]

        if success:
            LOG.info("Spring decompression successfully completed!")
            LOG.info(f"Time to decompress: {time_to_decompress}")
            return True

        LOG.error("Spring decompression failed")
        LOG.error(self.stderr)
        return False

    def compress(
        self, first: Path, second: Path, outfile: Path
    ) -> bool:
        """Run the spring compression command."""
        parameters = [
            "-c",
            "-i",
            str(first),
            str(second),
            "-o",
            str(outfile),
            "-t",
            str(self.threads),
        ]

        if first.suffix == ".gz":
            LOG.info("File(s) are gzipped")
            parameters.append("-g")

        if self.tmp:
            parameters.extend(["--working-dir", self.tmp])

        LOG.info("Compressing FASTQ to Spring")
        self.run_command(parameters)
        success = False
        time_to_compress = "unknown"
        for line in self.stdout_lines():
            line = line.lower()
            if "compression done" in line:
                success = True
            if "total time for compression" in line:
                time_to_compress = line.split(" ")[-2]

        if success:
            LOG.info("Spring compression successfully completed!")
            LOG.info(f"Time to compress: {time_to_compress}")
            return True

        LOG.error("Spring compression failed")
        LOG.error(self.stderr)
        return False

    def __repr__(self):
        return f"SpringProcess:base_call:{self.base_call}"


class CramProcess(Process):
    """Process to deal with CRAM commands."""

    def __init__(self, binary: str, refgenome_path: str, threads: int = 8):
        """Initialise a spring process."""
        super().__init__(binary)
        self.refgenome_path: str = refgenome_path
        self.threads: int = threads

    def decompress(self, cram_path: Path, bam_path: Path) -> bool:
        """Convert CRAM to BAM."""
        LOG.info(f"Decompressing cram {cram_path} to bam {bam_path}")
        parameters = [
            "view",
            "-b",
            "-o",
            str(bam_path),
            "-T",
            self.refgenome_path,
            str(cram_path),
        ]
        self.run_command(parameters)
        return True

    def compress(self, bam_path: Path, cram_path: Path) -> bool:
        """Convert BAM to CRAM."""
        LOG.info(f"Compressing BAN {bam_path} to CRAM {cram_path}")
        parameters = [
            "view",
            "-C",
            "-T",
            self.refgenome_path,
            str(bam_path),
            "-o",
            str(cram_path),
        ]
        self.run_command(parameters)
        self.index(cram_path)
        return True

    @staticmethod
    def get_index_path(file_path: Path) -> Path:
        """Create a index path based on a file name."""
        index_suffix = ".bai" if file_path.suffix == ".bam" else ".crai"
        return file_path.with_suffix(file_path.suffix + index_suffix)

    def index(self, file_path: Path):
        """Index a BAM or CRAM file."""
        LOG.info(f"Creating index for {file_path}")
        index_path = self.get_index_path(file_path)
        parameters = ["index", str(file_path), str(index_path)]
        self.run_command(parameters)

    def self_check(self):
        """Run a check and see that all parameters are valid."""
        LOG.info("Check that Cram process is correctly initialized.")
        if self.refgenome_path is None:
            LOG.warning("Please specify the path to a reference genome")
            raise SyntaxError
        if not Path(self.refgenome_path).exists():
            LOG.warning("Reference genome %s does not exist", self.refgenome_path)
            raise FileNotFoundError

    def __repr__(self):
        return f"CramProcess:base_call:{self.base_call}, refgenome_path:{self.refgenome_path}"
