#!/bin/bash

cd /home/jack/2capcha_1point3acres/1point3acres/src

echo -e "\n$(date) - Starting script execution:" >> /home/jack/2capcha_1point3acres/OUTPUTs/1point3acres.log

$new_output=$(python3 server.py)

echo "$new_output" >> /home/jack/2capcha_1point3acres/OUTPUTs/1point3acres.log 2>&1

if [[ $new_output == *"Traceback"* ]]; then
    echo -e " - Error in script execution, trying again:" >> /home/jack/2capcha_1point3acres/OUTPUTs/1point3acres.log
    echo -e "$new_output" >> /home/jack/2capcha_1point3acres/OUTPUTs/1point3acres.log
else
    echo -e " - code executed successfully" >> /home/jack/2capcha_1point3acres/OUTPUTs/1point3acres.log
fi