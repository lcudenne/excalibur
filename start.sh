#!/bin/bash

if [ ! -d "venv" ]
then
    python3 -m venv venv &> /dev/null
    source venv/bin/activate &> /dev/null
    pip install -r excalibur/requirements.txt &> /dev/null
else
    source venv/bin/activate &> /dev/null
fi

PYTHONPATH+=. python3 excalibur/app.py $@ &> excalibur.log

deactivate &> /dev/null

exit 0
