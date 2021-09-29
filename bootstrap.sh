#!/bin/bash
export FLASK_APP=./src/main.py
source ./venv/scripts/activate
flask run -h 0.0.0.0 # localhost testing