#!/bin/bash --login
set -e

conda activate aip
export force_color_prompt=yes
exec "$@"
