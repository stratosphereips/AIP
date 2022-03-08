#!/bin/bash --login
set -e

conda activate $HOME/AIP/env
exec "$@"
