#!/bin/bash

if [ -f received_data.txt ]; then
    echo "received_data.txt removed"
    rm received_data.txt
else
    echo "received_data.txt does not exist"
fi

echo "Running flask_app.py for 12 seconds..."
timeout 12s python3 flask_app.py

sleep 1

cat received_data.txt | grep '10.100.25.22' received_data.txt | cut -d' ' -f1,2 | cut -d'.' -f1 | sort | uniq -c

