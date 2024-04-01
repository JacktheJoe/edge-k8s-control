#!/bin/bash

# Allocate ~500 MB of RAM
allocate_memory() {
    # Generate a string of size ~500 MB (524288000 bytes)
    # Note: Adjust the size if needed to be more precise
    MEMORY_BLOCK=$(head -c 524288000 < /dev/zero | tr '\0' 'a')
}

# Call the function to allocate memory
# allocate_memory

# Infinite loop to send the heartbeat update
while true; do
    curl -X POST http://10.100.20.10:23333/data -d '    Heartbeat Update    ' -H "Content-Type: text/plain"
    sleep 0.1
done
