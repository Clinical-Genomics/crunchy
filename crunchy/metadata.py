"""Functions that collects metadata"""

import json
import logging
from pathlib import Path

from crunchy.integrity import get_checksum

LOG = logging.getLogger(__name__)


def get_fastq_info(fastq: Path, tag: str, algorithm) -> dict:
    """Get the necessary information about a fastq file and return it in a dict"""
    fastq_info = {"file": tag}
    fastq_info["checksum"] = get_checksum(infile=fastq, algorithm=algorithm)
    fastq_info["path"] = str(fastq.absolute())
    fastq_info["algorithm"] = algorithm

    return fastq_info


def fetch_spring_metadata(
    first_read: Path, second_read: Path, spring: Path, algorithm: str = "sha256"
) -> list:
    """Create metadata for a spring archive

    This means that for each file the original paths and checksums are stored in a dict.
    """
    metadata = []
    metadata.append(get_fastq_info(first_read, "first_read", algorithm))
    metadata.append(get_fastq_info(second_read, "second_read", algorithm))
    metadata.append({"path": str(spring.absolute()), "file": "spring"})

    return metadata


def dump_spring_metadata(metadata: list) -> Path:
    """Write spring metadata to json file

    Path to metadata is the same as the path to spring archive with suffix .json instead of .spring

    Returns:
        metadata_path
    """
    spring_path = None
    for file_info in metadata:
        if file_info["file"] == "spring":
            spring_path = Path(file_info["path"])

    metadata_path = spring_path.with_suffix(".json")
    with open(metadata_path, "w") as out:
        LOG.info("Dumping spring metadata to %s", metadata_path)
        json.dump(metadata, out, indent=2)
    return metadata_path
