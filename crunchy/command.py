"""
Code to handle communications to the shell
"""

import copy
import logging
import pathlib
import subprocess
from subprocess import CalledProcessError

LOG = logging.getLogger(__name__)


class Process:
    """Class to handle communication with other programs via the shell

    The other parts of the code should not need to have any knowledge about how the processes are
    called, that will be handled in this module.Output form stdout and stdin will be handeld here.
    """

    def __init__(self, binary, config=None, config_parameter="--config"):
        """
        Args:
            binary(str): Path to binary for the process to use
            config(str): Path to config if used by process
        """
        super(Process, self).__init__()
        self.binary = binary
        LOG.debug("Initialising Process with binary: %s", self.binary)
        self.base_call = [self.binary]
        if config:
            self.base_call.extend([config_parameter, config])
        LOG.debug("Use base call %s", self.base_call)
        self._stdout = ""
        self._stderr = ""

    def run_command(self, parameters=None):
        """Execute a command in the shell

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
            LOG.critical("Call %s exit with a non zero exit code", command)
            LOG.critical(self.stderr)
            raise CalledProcessError(command, res.returncode)

        return res.returncode

    @property
    def stdout(self):
        """Fetch stdout"""
        return self._stdout

    @stdout.setter
    def stdout(self, text):
        self._stdout = text

    @stdout.deleter
    def stdout(self):
        del self._stdout

    @property
    def stderr(self):
        """Fetch stderr"""
        return self._stderr

    @stderr.setter
    def stderr(self, text):
        self._stderr = text

    @stderr.deleter
    def stderr(self):
        del self._stderr

    def stdout_lines(self):
        """Iterate over the lines in self.stdout"""
        for line in self.stdout.split("\n"):
            yield line

    def stderr_lines(self):
        """Iterate over the lines in self.stderr"""
        for line in self.stderr.split("\n"):
            yield line

    def __repr__(self):
        return f"Process:base_call:{self.base_call}"


class SpringProcess(Process):
    """Process to deal with spring commands"""

    def __init__(self, binary, threads=8, tmp_dir=None):
        """Initialise a spring process"""
        super().__init__(binary)
        self.threads = threads
        self.tmp = tmp_dir

    def decompress(
        self, spring_path: pathlib.Path, first: pathlib.Path, second: pathlib.Path
    ) -> bool:
        """Run the spring decompress command"""
        parameters = ["-d", "-i", str(spring_path), "-o", str(first), str(second)]
        if first.suffix == ".gz":
            LOG.info("Compressing to gzipped format")
            parameters.append("-g")

        if self.tmp is not None:
            parameters.extend(["--working-dir", self.tmp])

        LOG.info("Decompressing spring compressed file")
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
            LOG.info("Spring decompression succesfully completed!")
            LOG.info("Time to decompress: %s", time_to_decompress)
            return True

        LOG.error("Spring decompression failed")
        LOG.error(self.stderr)
        return False

    def compress(
        self, first: pathlib.Path, second: pathlib.Path, outfile: pathlib.Path
    ) -> bool:
        """Run the spring compression command"""
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

        if self.tmp is not None:
            parameters.extend(["--working-dir", self.tmp])

        LOG.info("Compressing fastq to spring")
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
            LOG.info("Spring compression succesfully completed!")
            LOG.info("Time to compress: %s", time_to_compress)
            return True

        LOG.error("Spring compression failed")
        LOG.error(self.stderr)
        return False

    def __repr__(self):
        return f"SpringProcess:base_call:{self.base_call}"


class CramProcess(Process):
    """Process to deal with cram commands"""

    def __init__(self, binary: str, refgenome_path: str, threads=8):
        """Initialise a spring process"""
        super().__init__(binary)
        self.refgenome_path = refgenome_path
        self.threads = threads

    def decompress(self, cram_path: pathlib.Path, bam_path: pathlib.Path) -> bool:
        """Convert cram to bam"""
        LOG.info("Decompressing cram %s to bam %s", cram_path, bam_path)
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

    def compress(self, bam_path: pathlib.Path, cram_path: pathlib.Path) -> bool:
        """Convert bam to cram"""
        LOG.info("Compressing bam %s to cram %s", bam_path, cram_path)
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
    def get_index_path(file_path: pathlib.Path) -> pathlib.Path:
        """Create a index path based on a file name"""
        index_suffix = ".crai"
        if file_path.suffix == ".bam":
            index_suffix = ".bai"
        return file_path.with_suffix(file_path.suffix + index_suffix)

    def index(self, file_path: pathlib.Path):
        """Index a bam or cram file"""
        LOG.info("Creating index for %s", file_path)
        index_path = self.get_index_path(file_path)
        parameters = ["index", str(file_path), str(index_path)]
        self.run_command(parameters)

    def __repr__(self):
        return f"CramProcess:base_call:{self.base_call}, refgenome_path:{self.refgenome_path}"
