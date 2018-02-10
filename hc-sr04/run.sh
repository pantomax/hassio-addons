#!/bin/bash
set -e
 
code=$(cat /data/options.json | jq -r '.code')
py2=$(cat /data/options.json | jq -r '.python2 // empty')

PYTHON=$(which python3)

if [ "${py2}" == "true" ];
then
    PYTHON=$(which python2)
fi

fi
python ${code} 
