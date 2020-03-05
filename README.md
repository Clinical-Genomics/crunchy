[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
![Build Status - GitHub](https://github.com/Clinical-Genomics/crunchy/workflows/Build/badge.svg)

# Crunchy

A python wrapper around [spring][spring] to compress fastq and check the integrity.

## Install

```
git clone https://github.com/Clinical-Genomics/crunchy
pip install -e .
crunchy --help
Usage: crunchy [OPTIONS] COMMAND [ARGS]...

  Base command for crunchy

Options:
  --spring-binary TEXT            Path to spring binary  [default: spring]
  -t, --threads INTEGER           Number of threads to use for spring
                                  compression  [default: 8]
  --log-level [DEBUG|INFO|WARNING]
                                  Choose what log messages to show
  --help                          Show this message and exit.

Commands:
  auto        Recursively find all fastq pairs below a directory and spring...
  checksum    Create a checksum for the file(s)
  compress    Compress a file
  decompress  Decompress a file
```

## Workflow

Each command can be run separately. To compress all fastq pairs below a directory run `crunchy auto <path_to_dir>`.

1. **Recursively find all fastq pairs**

1. **Compress all pairs with spring**
```file_1.fastq + file_2.fastq (spring)-> file.spring```

1. **Decompress with spring**
```file.spring (spring)-> file_1.fastq + file_2.fastq```

1. **Compare checksum with previous**
```file_1.fastq + file_2.fastq (hashlib)-> compare```

1. **Delete fastq** (If the compression was lossless)
```file_1.fastq + file_2.fastq (rm)->```

[spring]: https://github.com/shubhamchandak94/Spring