FROM python:3.12-slim AS builder

# Create a non-root user
ARG username=aip
ARG uid=1000
ARG gid=1000

ENV USER=$username
ENV UID=$uid
ENV GID=$gid
ENV HOME=/home/$USER

RUN apt-get update && \
    apt-get install -y python3-venv && \
    rm -rf /var/lib/apt/lists/*

RUN groupadd -g $GID $USER && \
    useradd -m -u $UID -g $GID -s /bin/bash $USER

# Switch to the non-root user
USER $USER

WORKDIR $HOME/AIP

COPY requirements.txt .

RUN python -m venv venv && \
    ./venv/bin/pip install --no-cache-dir -r requirements.txt

# Remove unnecessary files
RUN find venv/ -type d -name '__pycache__' -exec rm -rf {} +
RUN find venv/ -type d -name 'tests' -exec rm -rf {} + && \
    find venv/ -type d -name '*.dist-info' -exec rm -rf {} +

# Stage 2: Final stage
FROM python:3.12-slim

# Create a non-root user
ARG username=aip
ARG uid=1000
ARG gid=1000

ENV USER=$username
ENV UID=$uid
ENV GID=$gid
ENV HOME=/home/$USER

RUN groupadd -g $GID $USER && \
    useradd -m -u $UID -g $GID -s /bin/bash $USER

# Copy the entrypoint script
COPY etc/docker/entrypoint.sh /usr/local/bin/
RUN chmod u+x /usr/local/bin/entrypoint.sh

# Switch to the non-root user
USER $USER

WORKDIR $HOME/AIP

# Copy venv from the builder stage
COPY --from=builder $HOME/AIP/venv $HOME/AIP/venv

# Copy aip files 
COPY --chown=$USER:$USER . .

ENV PATH="$HOME/AIP/venv/bin:$PATH"

ENTRYPOINT [ "/usr/local/bin/entrypoint.sh" ]
