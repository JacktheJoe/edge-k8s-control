## automate the checkpoint and restore process

#### needed:

1. prep
   1. method of untaint master for receive deployment of monitor and automation pod
   2. custom scheduler for the above use case (maybe only allow deployment with "system-wide" tag?)
   3. communciation inside the cluster
   4. inter-cluster discovery? or maybe this should be part of the wireless setup
2. sender's end
   1. endpoint location on master nodes
   2. original yaml file, as one can't just delete the pod (deployment will make sure there always exist at least one pod instance)
   3. name of exact pod (for example, name is counter, but actual pod name is counter-85b5d4df98-7qjgk)
   4. namespace of where the pod is located --> could be a dictionary of where the service belong to, for example, ml namespace for ml apps
   5. the original pod/deployment's base image --> in case of N.E, pull: this could be resolved from yaml file
   6. commuication to current cluster's worker nodes
   7. trigger checkpoint from the master node
   8. communicate to corrosponding worker
3. receiver's end
   1. https endpoint for receiving data (might be able to use the crts from sender's curl commands)
   2. checkpoint