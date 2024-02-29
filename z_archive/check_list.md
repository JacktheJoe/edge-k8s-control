</t> # update: iperf should be done on the oponent side's peer-update script:
</t> </t> reason can be for the ease of updating

- [x] take out port -> env variables
- [x] add bandwidth testing with iperf 
- [x] consider that some node that might not be directly reachable by other nodes in the system -- this should be fine as baseline infrastructure will be set
- [x] append sent_data to log
- [x] construct new metric with bw/latency from ping and iperf
- [x] maybe take the ping results out and for peer place it inside peer-update.py
- [ ] re-write the update logic interms of what to update and keep log from
- [ ] re-write part of logic to perform devision making on the project
- [ ] re-write the redirection logic with bash or python, implement DISCO's max/current_hop idea
- [ ] 
- [ ] 
- [ ] test changed code