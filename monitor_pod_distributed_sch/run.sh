#!/bin/bash

# export necessary environment variables, and start iperf server to receive testing
prep(){
    # filter out the cpu score per thread
    if ! CPU_CORE_PT=$(sysbench cpu --cpu-max-prime=20000 --threads=1 run | grep -oP 'events per second:\s+\K\d+\.\d+' | grep -oP '\d+\.\d+'); then
        printf "Failed to get CPU core performance per thread\n" >&2
        return 1
    fi
    export CPU_CORE_PT

    # filter out the total number of cpu vcores (threads) in the system
    if ! CPU_CORECOUNT=$(grep "cpu cores" /proc/cpuinfo | head -n 1 | awk '{print $4}'); then
        printf "Failed to get CPU core count\n" >&2
        return 1
    fi
    export CPU_CORECOUNT

    # updated to using external node's IP variable
    if ! subnet=$(echo "$NODE_IP" | awk 'BEGIN{FS=OFS="."}{NF--; print $0}'); then
        printf "Failed to parse NODE_IP for subnet\n" >&2
        return 1
    fi
    SUBNET="${subnet}.0/24"
    export SUBNET

    [[ ! -f $NETWORK_LOG ]] && touch "$NETWORK_LOG"
    [[ ! -f $METRIC_LOG ]] && touch "$METRIC_LOG"
    [[ ! -f $DECISION_LOG ]] && touch "$DECISION_LOG"
    [[ ! -f $DEPLOYMENT_LOG ]] && touch "$DEPLOYMENT_LOG"

    # start the iperf server for testing
    if ! iperfserver; then
        printf "Failed to start iperf server\n" >&2
        return 1
    fi
}

iperfserver(){
    iperf -s -i 5 -p "$IPERF_SERVER_PORT" &
}

startmetricupdate(){
    python3 metric_update.py &

}

startreceiveforward(){
    python3 receive_forward.py &
}

startreceivingdeployment(){
    python3 deployment_request.py &
}


# start preparation
if ! prep; then
    printf "Preparation failed\n" >&2
    exit 1
fi

# start running resource & network metric collections
if ! startmetricupdate; then
    printf "Failed to start metric update\n" >&2
    exit 1
fi

# start receive metric and forwarding
if ! startreceiveforward; then
    printf "Failed to start receive forward\n" >&2
    exit 1
fi

# start receive deployment
if ! startreceivingdeployment; then
    printf "Failed to start receive deployment\n" >&2
    exit 1
fi

sleep infinity
