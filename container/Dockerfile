################## BASE IMAGE ######################

FROM clinicalgenomics/mip:2.0"

################## METADATA ######################

LABEL base_image="clinicalgenomics/mip:2.0""
LABEL version="1"
LABEL software="crunchy"
LABEL software.version="0.5"
LABEL extra.binaries="crunchy"

################## MAINTAINER ######################
MAINTAINER Clinical-Genomics

RUN conda install python=3.7 pip samtools=1.10=h9402c20_2 spring=1.0=he513fc3_0

## Clean up after conda
RUN /opt/conda/bin/conda clean -tipsy

RUN pip install --no-cache-dir crunchy==0.5

WORKDIR /data/
