![Build Status - GitHub](https://github.com/Clinical-Genomics/crunchy/workflows/Build/badge.svg)

# Crunchy

A python wrapper around [spring][spring] to compress fastq and check the integrity.

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