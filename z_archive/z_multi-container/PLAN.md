list of containers:
1. metric-collection
    - start network metric server
    - pull resource metric information from metric API
    - performs network metric testing
    - constructs packet, send to sending-forwarding && storage-update container via POST
2. storage-update
    - writes received information locally
    - updates the data/log server
3. sending-forwarding
    - async, processes received message, send
4. receiving-processing
5. decision-logic
6. deployment
7. migration