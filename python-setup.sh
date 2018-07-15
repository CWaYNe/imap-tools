#!/bin/sh

python3 -m venv ./venv

# for freebsd c shell
source venv/bin/activate.csh

pip install -r ./requirements.txt