FROM python:3.12-slim
LABEL org.opencontainers.image.title="AIP" \
      org.opencontainers.image.description="This image runs the AIP framework for blocklist generation." \
      org.opencontainers.image.version="0.1.0" \
      org.opencontainers.image.created="2023-08-01" \
      org.opencontainers.image.source="https://github.com/stratosphereips/AIP" \
      org.opencontainers.image.source="Joaquin Bogado <joaquin.bogado@aic.fel.cvut.cz>" \
      org.opencontainers.image.authors="Veronica Valeros <valerver@fel.cvut.cz>"

ARG DEBIAN_FRONTEND=noninteractive
ENV TZ=Etc/UTC

SHELL [ "/bin/bash", "--login", "-c" ]

# Create a non-root user
ARG username=aip
ARG uid=1000
ARG gid=100
ENV USER $username
ENV UID $uid
ENV GID $gid
ENV HOME /home/$USER

RUN adduser --disabled-password \
    --gecos "Non-root user" \
    --uid $UID \
    --gid $GID \
    --home $HOME \
    $USER

RUN apt-get update && \
    apt-get install -y bzip2 wget && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

COPY etc/docker/entrypoint.sh /usr/local/bin/
RUN chmod u+x /usr/local/bin/entrypoint.sh

USER $USER

ENV MINICONDA_VERSION latest
ENV CONDA_DIR $HOME/miniconda3
RUN wget --quiet https://repo.anaconda.com/miniconda/Miniconda3-$MINICONDA_VERSION-Linux-x86_64.sh -O ~/miniconda.sh && \
    chmod +x ~/miniconda.sh && \
    ~/miniconda.sh -b -p $CONDA_DIR && \
    rm ~/miniconda.sh

# Make non-activate conda commands available
ENV PATH=$CONDA_DIR/bin:$PATH

# Make conda activate command available from /bin/bash --login shells
RUN echo ". $CONDA_DIR/etc/profile.d/conda.sh" >> ~/.profile

# Make conda activate command available from /bin/bash --interative shells
RUN conda init bash

ENV PROJECT_DIR $HOME/AIP
RUN mkdir $PROJECT_DIR
WORKDIR $PROJECT_DIR

COPY environment.yml requirements.txt $PROJECT_DIR/

ENV ENV_PREFIX $HOME/env
RUN conda update --name base conda
RUN conda env create --file $PROJECT_DIR/environment.yml --force
RUN conda clean --all --yes

# Include AIP as python package
COPY . $PROJECT_DIR
RUN ln -s /home/aip/AIP/lib/aip /home/aip/miniconda3/envs/aip/lib/python3.11/site-packages/

RUN echo 'conda activate aip' >> $HOME/.bashrc

ENTRYPOINT [ "/usr/local/bin/entrypoint.sh" ]
