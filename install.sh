#!/bin/sh

mkdir -p ~/.qm
cp -n config.json.example ~/.qm/config.json
mkdir -p ~/bin
ln -s "$(pwd)/qm.py" ~/bin/qm
