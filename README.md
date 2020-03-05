# Crunchy

A python wrapper around [spring][spring] to compress fastq.

## Workflow

### Step 1 Unzip fastq files
`file_1.fastq.gz + file_2.fastq.gz` (gzip)-> `file_1.fastq + file_2.fastq`

### Step 2 Calculate md5 checksum
`file_1.fastq + file_2.fastq` (hashlib)-> `md5_1, md5_2`

### Step 3 Compress with spring
`file_1.fastq + file_2.fastq` (spring)-> `file.spring`

### Step 4 Decompress with spring
`file.spring` (spring)-> `file_1.fastq + file_2.fastq`

### Step 4 Compare checksum with previous
`file_1.fastq + file_2.fastq` (hashlib)-> `compare`

### Step 5 Delete fastq
`file_1.fastq + file_2.fastq` (rm)->