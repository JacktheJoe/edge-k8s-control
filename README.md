## Goal of this project

To test and experiment possible approaches to perform low-latency service migration for edge kubernetes clusters in a non-centralized mannor

### Plan of this project
 - CRIU for container/pod checkpoint and restores (require CRI-O as runtime for Kubernetes, as containerd is yet to include CRIU function)
 - layered cacheing for container image pre-loading
 - selected resource metric sharing
 - custom/modified scheduler to handle/enhance scheduling function for pod deployment/migration

### environment used
 - operating system: 
   - ubuntu 22.04 LTS:
     - problem: package conflicts and can only enable checkpoint, no restore, as restoring a checkpoint in kubernetes requires the use of buildah and build from scratch
   - ubuntu 20.04 LTS:
     - no such package conflicts anymore, also upgraded to kernel 5.15 for CRIU support

 - initial testing:
   - with 5 clusers of 3 nodes (1 master + 2 workers)
   - a data server to log

 - hypervisor and network:
   - proxmox + pfsense
     - proxmox used for running virtual machines
     - pfsense used for isolating traffic and perform rules to restrict or redirect, also enabling VPN connection to all nodes
       - each cluster inside its own subnet of 10.100.2x.1/24
       - data server location of 10.100.20.10 for logging

 - storage:
   - truenas core
     - mirrored ssd setup to prevent all-in-boom (the previous ubuntu 22 situation)