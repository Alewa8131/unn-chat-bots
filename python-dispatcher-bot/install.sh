#!/usr/bin/env bash

python3 -m venv .venv
source .venc/bin/activate
pip install -r requirements.txt
deactivate
