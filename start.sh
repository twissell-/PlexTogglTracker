#!/bin/bash -eu
set -o pipefail

# A minimal script to cron and ensure the flask server is always running.
#
# # rin
# * * * * * /home/twissell/bin/rin/start.sh
# 0 0 * * * [ -f /home/twissell/bin/rin/screen/log ] && rm /home/twissell/bin/rin/screen/log

RIN_DIR="/home/twissell/bin/rin"
start_command="screen -L -Logfile ${RIN_DIR}/screen/log -dmS rin ${RIN_DIR}/venv/bin/python ${RIN_DIR}/run.py"

if ! pgrep -if "${start_command}" &> /dev/null; then
    cd "${RIN_DIR}"
    export SCREENDIR="${RIN_DIR}/screen"
    $start_command
fi
