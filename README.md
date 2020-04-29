[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
![Build Status - GitHub](https://github.com/Clinical-Genomics/crunchy/workflows/Build/badge.svg)
[![codecov](https://codecov.io/gh/Clinical-Genomics/crunchy/branch/master/graph/badge.svg)](https://codecov.io/gh/Clinical-Genomics/crunchy)
[![CodeFactor](https://www.codefactor.io/repository/github/clinical-genomics/crunchy/badge)](https://www.codefactor.io/repository/github/clinical-genomics/crunchy)

# Crunchy

A python wrapper around [spring][spring] and cram (samtools) to compress fastq to spring and bam to cram. When compressing fastqs to spring an integrity check can be performed by using flag: `crunchy compress spring --spring-path <springfile> --first <read_1.fastq>  --second <read_2.fastq> --check-integrity`

## Install

### Pip
```
pip install crunchy
```

### Docker
This will install crunchy as well as samtools and spring within the container.
```
docker pull clinicalgenomics/crunchy:0.5
```
Run crunchy using:
```
docker run clinicalgenomics/crunchy:0.5 crunchy
```

### Developers
```
git clone https://github.com/Clinical-Genomics/crunchy
pip install -e .
crunchy --help
Usage: crunchy [OPTIONS] COMMAND [ARGS]...

  Base command for crunchy

                .---. .---.
               :     : o   :    me want cookie!
           _..-:   o :     :-.._    /
       .-''  '  `---' `---' "   ``-.
     .'   "   '  "  .    "  . '  "  `.
    :   '.---.,,.,...,.,.,.,..---.  ' ;
    `. " `.                     .' " .'
     `.  '`.                   .' ' .'
      `.    `-._           _.-' "  .'  .----.
        `. "    '"--...--"'  . ' .'  .'  o   `.
        .'`-._'    " .     " _.-'`. :       o  :
      .'      ```--.....--'''    ' `:_ o       :
    .'    "     '         "     "   ; `.;";";";'
   ;         '       "       '     . ; .' ; ; ;
  ;     '         '       '   "    .'      .-'
  '  "     "   '      "           "    _.-'

Options:
  --spring-binary TEXT            Path to spring binary  [default: spring]
  --samtools-binary TEXT          Path to spring binary  [default: samtools]
  -t, --threads INTEGER           Number of threads to use for spring
                                  compression  [default: 8]
  -r, --reference TEXT            Path to reference genome
  --log-level [DEBUG|INFO|WARNING]
                                  Choose what log messages to show
  --tmp-dir TEXT                  If specific temp dir should be used
  --help                          Show this message and exit.

Commands:
  auto        Run whole pipeline by compressing, comparing and deleting...
  compare     Compare two files by generating checksums.
  compress    Compress genomic files
  decompress  Decompress genomic files
```

## Workflow

Each command can be run separately. To compress all fastq pairs below a directory run `crunchy auto spring <path_to_dir>`.

1. **Recursively find all fastq pairs**

1. **Compress all pairs with spring**
```file_1.fastq + file_2.fastq (spring)-> file.spring```

1. **Decompress with spring**
```file.spring (spring)-> file_1.spring.fastq + file_2.spring.fastq```

1. **Compare checksum with previous**
```file_1.spring.fastq + file_1.fastq (hashlib)-> compare```

1. **Delete fastq** (If the compression was lossless)
```file_1.fastq + file_2.fastq (rm)->```

[spring]: https://github.com/shubhamchandak94/Spring
