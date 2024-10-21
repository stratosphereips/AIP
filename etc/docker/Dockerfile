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

# Define arguments for username, UID, and GID
ARG username=aip
ARG uid=1000
ARG gid=1000

# Set environment variables based on these arguments
ENV USER=$username
ENV UID=$uid
ENV GID=$gid
ENV HOME=/home/$USER

# Create a group and user based on the UID and GID
RUN groupadd -g $GID $USER && \
    useradd -m -u $UID -g $GID -s /bin/bash $USER

COPY etc/docker/entrypoint.sh /usr/local/bin/
RUN chmod u+x /usr/local/bin/entrypoint.sh

USER $USER
ENV PATH="$HOME/miniconda3/bin:$PATH"
ENV ENV_PREFIX=$HOME/env


# Conda installation and setup
RUN python -c "import urllib.request; urllib.request.urlretrieve('https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh', '$HOME/miniconda.sh')" && \
    bash ~/miniconda.sh -b -p $HOME/miniconda3 && \
    rm ~/miniconda.sh

RUN conda init bash

# Set the working directory
WORKDIR $HOME/AIP

COPY environment.yml requirements.txt .

RUN conda update --name base conda
RUN conda env create --file environment.yml && \
    conda clean --all --yes

# Include AIP as python package
COPY . $PROJECT_DIR
RUN ln -s /home/aip/AIP/lib/aip /home/aip/miniconda3/envs/aip/lib/python3.11/site-packages/

RUN echo 'conda activate aip' >> $HOME/.bashrc

ENTRYPOINT [ "/usr/local/bin/entrypoint.sh" ]
