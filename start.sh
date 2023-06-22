#!/bin/bash -eu
set -o pipefail

# A minimal script to cron on my seedbox to ensure the flask server is always running.

start_command="screen -t rin -d -m /home/twissell/bin/rin/venv/bin/python /home/twissell/bin/rin/run.py"

if ! pgrep -if "${start_command}" &> /dev/null; then
    $start_command
fi
