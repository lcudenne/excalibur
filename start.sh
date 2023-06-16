#!/bin/bash

if [ ! -d "venv" ]
then
    python3 -m venv venv &> /dev/null
fi

source venv/bin/activate &> /dev/null
pip install -r excalibur/requirements.txt &> /dev/null

PYTHONPATH+=. python3 excalibur/app.py $@ &> excalibur.log

deactivate &> /dev/null

exit 0
