#!/usr/bin/env bash

set -euxo pipefail

export TELEMETRY_ENABLED=false

function do_export () {
    template=$1
    mkdir ~/"$template"
    cd ~/"$template"
    rm -rf ~/.local/share/nextpy ~/"$template"/.web
    nextpy init --template "$template"
    nextpy export
}

echo "Preparing test project dir"
python3 -m venv ~/venv
source ~/venv/bin/activate

echo "Installing nextpy from local repo code"
pip install /nextpy-repo

echo "Running nextpy init in test project dir"
do_export blank
do_export base