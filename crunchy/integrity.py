"""Code to handle integrity of files"""

import gzip
import hashlib
import logging
import pathlib

LOG = logging.getLogger(__name__)


def compare_elements(elements):
    """Check if all elements are the same"""
    if len(set(elements)) == 1:
        return True
    return False


def get_checksum(infile: pathlib.Path, algorithm: str = "sha256"):
    """Get the checksum for a file"""
    LOG.info("Create checksum for %s", infile)
    if algorithm == "sha1":
        LOG.info("Use sha1")
        hash_obj = hashlib.sha1()
    elif algorithm == "md5":
        LOG.info("Use md5")
        hash_obj = hashlib.md5()
    else:
        LOG.info("Use sha256")
        hash_obj = hashlib.sha256()

    content = open(infile, "rb")
    if infile.suffix in [".gz", ".gzip"]:
        LOG.info("Unzip before counting checksum")
        content = gzip.open(infile, "rb")

    return generate_checksum(content, hash_obj)


def generate_checksum(content, hash_obj):
    """Return the checksum of a file

    Args:
        content(iterable)
        hash_obj
    """
    for chunk in iter(lambda: content.read(4096), b""):
        hash_obj.update(chunk)
    LOG.info("Checksum created")
    return hash_obj.hexdigest()
