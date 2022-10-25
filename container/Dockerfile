################## BASE IMAGE ######################

FROM clinicalgenomics/mip:2.0"

################## METADATA ######################

LABEL base_image="clinicalgenomics/mip:2.0""
LABEL version="2"
LABEL software="crunchy"
LABEL software.version="0.6.3"
LABEL extra.binaries="crunchy"

################## MAINTAINER ######################
MAINTAINER Clinical-Genomics

RUN conda install python=3.10 pip samtools=1.10=h9402c20_2 spring=1.0=he513fc3_0

## Clean up after conda
RUN /opt/conda/bin/conda clean -tipsy

RUN pip install --no-cache-dir crunchy==0.6.3

WORKDIR /data/
