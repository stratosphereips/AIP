#!/bin/bash --login

# Exit immediately if any command exits with a non-zero status
set -e

# Force the command prompt to display colors
export force_color_prompt=yes

# Activate the virtual environment
source "$HOME/AIP/venv/bin/activate"


# Execute any command passed to the container when run
PYTHONPATH="$HOME/AIP/lib:$PYTHONPATH" python "$@"

