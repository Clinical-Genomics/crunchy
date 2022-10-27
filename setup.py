"""Based on https://github.com/kennethreitz/setup.py"""


import contextlib
import io
import os
import sys
from shutil import rmtree

from setuptools import Command, find_packages, setup

# Package meta-data.
NAME = "crunchy"
DESCRIPTION = "Compress fastq with spring"
URL = "https://github.com/Clinical-Genomics/crunchy"
EMAIL = "henrik.stranneheim@scilifelab.com"
AUTHOR = "Mans Magnusson"
REQUIRES_PYTHON = ">=3.9.0"
VERSION = None

HERE = os.path.abspath(os.path.dirname(__file__))


def parse_reqs(req_path="./requirements.txt"):
    """Recursively parse requirements from nested pip files."""
    install_requires = []
    with io.open(os.path.join(HERE, req_path), encoding="utf-8") as handle:
        # remove comments and empty lines
        lines = (
            line.strip() for line in handle if line.strip() and not line.startswith("#")
        )

        for line in lines:
            if line.startswith("-i") or line.startswith("-e"):
                continue
            # check for nested requirements files
            if line.startswith("-r"):
                # recursively call this function
                install_requires += parse_reqs(req_path=line[3:])

            else:
                # add the line as a new requirement
                install_requires.append(line)

    return install_requires


# What packages are required for this module to be executed?
REQUIRED = parse_reqs()

# What packages are optional?
EXTRAS = {}

# The rest you shouldn't have to touch too much :)
# ------------------------------------------------
# Except, perhaps the License and Trove Classifiers!
# If you do change the License, remember to change the Trove Classifier for that!


# Import the README and use it as the long-description.
# Note: this will only work if 'README.md' is present in your MANIFEST.in file!
try:
    with io.open(os.path.join(HERE, "README.md"), encoding="utf-8") as f:
        LONG_DESCRIPTION = "\n" + f.read()
except FileNotFoundError:
    LONG_DESCRIPTION = DESCRIPTION

# Load the package's __version__.py module as a dictionary.
ABOUT = {}
if not VERSION:
    with open(os.path.join(HERE, NAME, "version.py")) as f:
        exec(f.read(), ABOUT)
else:
    ABOUT["__version__"] = VERSION


class UploadCommand(Command):
    """Support setup.py upload."""

    description = "Build and publish the package."
    user_options = []

    @staticmethod
    def status(s):
        """Prints things in bold."""
        print("\033[1m{0}\033[0m".format(s))

    def initialize_options(self):
        """Set or (reset) all options/attributes/caches used by the command to their default values."""
        pass  # currentlu, nothing needs resetting

    def finalize_options(self):
        """Set final values for all options/attributes used by the command."""
        pass  # currently, nothing no final values needs to be set

    def run(self):
        with contextlib.suppress(OSError):
            self.status("Removing previous builds…")
            rmtree(os.path.join(HERE, "dist"))
        self.status("Building Source and Wheel (universal) distribution…")
        os.system("{0} setup.py sdist bdist_wheel --universal".format(sys.executable))

        self.status("Uploading the package to PyPI via Twine…")
        os.system("twine upload dist/*")

        self.status("Pushing git tags…")
        os.system("git tag v{0}".format(ABOUT["__version__"]))
        os.system("git push --tags")

        sys.exit()


# Where the magic happens:
setup(
    name=NAME,
    version=ABOUT["__version__"],
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    author=AUTHOR,
    author_email=EMAIL,
    python_requires=REQUIRES_PYTHON,
    url=URL,
    packages=find_packages(exclude=("tests",)),
    entry_points={"console_scripts": ["crunchy = crunchy.__main__:base_command"]},
    install_requires=REQUIRED,
    extras_require=EXTRAS,
    include_package_data=True,
    license="MIT",
    keywords=["vcf", "compression"],
    classifiers=[
        # Trove classifiers
        # Full list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Unix",
        "Intended Audience :: Science/Research",
    ],
    # $ setup.py publish support.
    cmdclass={"upload": UploadCommand},
)
