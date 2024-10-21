#!/bin/bash --login

# Exit immediately if any command exits with a non-zero status
set -e

# Force the command prompt to display colors
export force_color_prompt=yes

# Initialize Conda in the current shell session
source $HOME/miniconda3/etc/profile.d/conda.sh

# Activate the conda environment already created in the docker
conda activate aip

# Execute any command passed to the container when run
exec "$@"
