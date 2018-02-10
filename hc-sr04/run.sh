#!/bin/bash
set -e
 
requirements=$(cat /data/options.json | jq -r 'if .requirements then .requirements | join(" ") else "" end')
code=$(cat /data/options.json | jq -r '.code')
clean=$(cat /data/options.json | jq -r '.clean //empty')
py2=$(cat /data/options.json | jq -r '.python2 // empty')

PYTHON=$(which python3)

if [ "${py2}" == "true" ];
then
    PYTHON=$(which python2)
fi

fi
python ${code} 
