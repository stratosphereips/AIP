#!/bin/bash --login
set -e

source $HOME/miniconda3/etc/profile.d/conda.sh

conda activate aip
export force_color_prompt=yes
exec "$@"
