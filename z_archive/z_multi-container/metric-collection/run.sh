#!/bin/sh

# export necessary environment variables, and start iperf server to receive testing
prep(){
    # filter out the cpu score per thread
    export CPU_CORE_PT=$(sysbench cpu --cpu-max-prime=20000 --threads=1 run | grep -oP 'events per second:\s+\K\d+\.\d+' | grep -oP '\d+\.\d+')

    # filter out the total number of cpu vcores (threads) in the system
    export CPU_CORECOUNT=$(cat /proc/cpuinfo | grep "cpu cores" | head -n 1 | awk '{print $4}')

    # start the iperf server for testing
    # each connection for 5 minutes, 
    iperf -s -i 5 -p $IPERF_SERVER_PORT &
}
prep

# after all prep work, start running resource & network metric collections


sleep infinity
