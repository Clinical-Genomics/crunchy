"""Functions that collects metadata"""
import json
import logging
from pathlib import Path

from crunchy.integrity import get_checksum

LOG = logging.getLogger(__name__)


def fetch_spring_metadata(
    first_read: Path, second_read: Path, spring: Path, algorithm: str = "sha256"
) -> list:
    """Create metadata for a spring archive

    This means that for each file the original paths and checksums are stored in a dict.
    """
    metadata = []
    first_checksum = get_checksum(infile=first_read, algorithm=algorithm)
    metadata.append(
        {
            "path": str(first_read.absolute()),
            "file": "first_read",
            "checksum": first_checksum,
            "algorithm": algorithm,
        }
    )
    second_checksum = get_checksum(infile=second_read)
    metadata.append(
        {
            "path": str(second_read.absolute()),
            "file": "second_read",
            "checksum": second_checksum,
            "algorithm": algorithm,
        }
    )
    metadata.append({"path": str(spring.absolute()), "file": "spring"})

    return metadata


def dump_spring_metadata(metadata: list):
    """Write spring metadata to json file

    Path to metadata is the same as the path to spring archive with suffix .json instead of .spring
    """
    spring_path = None
    for file_info in metadata:
        if file_info["file"] == "spring":
            spring_path = Path(file_info["path"])

    metadata_path = spring_path.with_suffix(".json")
    with open(metadata_path, "w") as out:
        LOG.info("Dumping spring metadata to %s", metadata_path)
        json.dump(metadata, out, indent=2)
