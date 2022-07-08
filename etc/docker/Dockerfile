FROM ubuntu:focal
ARG DEBIAN_FRONTEND=noninteractive
ENV TZ=Etc/UTC

LABEL maintainer="Joaquin Bogado <joaquin.bogado@aic.fel.cvut.cz>"

SHELL [ "/bin/bash", "--login", "-c" ]

RUN apt-get update --fix-missing && \
    apt-get install -y wget bzip2 curl git vim argus-client&& \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

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

COPY environment.yml requirements.txt /tmp/
RUN chown $UID:$GID /tmp/environment.yml /tmp/requirements.txt

COPY etc/docker/entrypoint.sh /usr/local/bin/
RUN chown $UID:$GID /usr/local/bin/entrypoint.sh && \
    chmod u+x /usr/local/bin/entrypoint.sh

USER $USER

ENV MINICONDA_VERSION latest
ENV CONDA_DIR $HOME/miniconda3
RUN wget --quiet https://repo.anaconda.com/miniconda/Miniconda3-$MINICONDA_VERSION-Linux-x86_64.sh -O ~/miniconda.sh && \
    chmod +x ~/miniconda.sh && \
    ~/miniconda.sh -b -p $CONDA_DIR && \
    rm ~/miniconda.sh

# make non-activate conda commands available
ENV PATH=$CONDA_DIR/bin:$PATH

# make conda activate command available from /bin/bash --login shells
RUN echo ". $CONDA_DIR/etc/profile.d/conda.sh" >> ~/.profile

# make conda activate command available from /bin/bash --interative shells
RUN conda init bash

ENV PROJECT_DIR $HOME/AIP
RUN mkdir $PROJECT_DIR
WORKDIR $PROJECT_DIR


ENV ENV_PREFIX $HOME/env
RUN conda update --name base conda
RUN conda env create --file /tmp/environment.yml --force
RUN conda clean --all --yes

# Include AIP as python package
# RUN mkdir -p /home/aip/AIP/lib/python3.10/site-packages/
RUN ln -s /home/aip/AIP/lib/aip /home/aip/miniconda3/envs/aip/lib/python3.10/site-packages/

RUN echo 'conda activate aip' >> $HOME/.bashrc

ENTRYPOINT [ "/usr/local/bin/entrypoint.sh" ]

