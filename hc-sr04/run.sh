#!/bin/bash
set -e
 
code=$(cat /data/options.json | jq -r '.code')

if [ "${py2}" == "true" ];
then
    PYTHON=$(which python2)
fi

if [ "$clean" == "true" ];
then
rm -rf /data/venv/
fi

if [ ! -f "/data/venv/bin/activate" ];
then
    mkdir -p /data/venv/
    cd /data/venv
    virtualenv -p ${PYTHON} .
    . bin/activate
fi

python ${code} 
