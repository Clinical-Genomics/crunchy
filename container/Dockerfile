################## BASE IMAGE ######################

FROM python:3.10-slim

################## METADATA ######################

LABEL base_image="python:3.10-slim"
LABEL version="3"
LABEL software="crunchy"
LABEL software.version="1.0.2"
LABEL extra.binaries="crunchy"

################## MAINTAINER ######################
MAINTAINER Clinical-Genomics

RUN conda install python=3.10 pip samtools=1.16.1=h6899075_1 spring=1.0=he513fc3_0

## Clean up after conda
RUN /opt/conda/bin/conda clean -tipsy

RUN pip install --no-cache-dir crunchy==1.0.2

WORKDIR /data/
