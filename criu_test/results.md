## results for checkpointing:

### for container mem-dummy:
Mem-dummy just holds a lot of ram, for example, current config is about 746MiB of ram. 
meaningless, but a good thing to test relative performance -- however, since all resources are simulated and shared, timing might not be accurate

///////  for cluster 1
root@master-1:~# time curl -X POST "https://10.100.21.21:10250/checkpoint/default/mem-dummy-deployment-66db99f88f-95t2j/mem-dummy"  --insecure --cert /etc/kubernetes/pki/apiserver-kubelet-client.crt --key /etc/kubernetes/pki/apiserver-kubelet-client.key

{"items":["/var/lib/kubelet/checkpoints/checkpoint-mem-dummy-deployment-66db99f88f-95t2j_default-mem-dummy-2024-03-13T16:07:52Z.tar"]}
real	0m7.472s
user	0m0.010s
sys	0m0.006s
root@master-1:~# 
root@master-1:~# kubectl top pods
NAME                                    CPU(cores)   MEMORY(bytes)   
mem-dummy-deployment-66db99f88f-95t2j   0m           746Mi   

/////// for cluster 2
root@master-2:~# time curl -X POST "https://10.100.22.21:10250/checkpoint/default/mem-dummy-deployment-66db99f88f-nhjd5/mem-dummy"  --insecure --cert /etc/kubernetes/pki/apiserver-kubelet-client.crt --key /etc/kubernetes/pki/apiserver-kubelet-client.key
{"items":["/var/lib/kubelet/checkpoints/checkpoint-mem-dummy-deployment-66db99f88f-nhjd5_default-mem-dummy-2024-03-13T16:13:56Z.tar"]}
real	0m4.762s
user	0m0.013s
sys	0m0.003s
root@master-2:~# kubectl top pods
NAME                                    CPU(cores)   MEMORY(bytes)   
mem-dummy-deployment-66db99f88f-nhjd5   0m           746Mi

/////// for cluster 3
root@master-3:~# time curl -X POST "https://worker-3-2:10250/checkpoint/default/mem-dummy-deployment-66db99f88f-fzb22/mem-dummy"  --insecure --cert /etc/kubernetes/pki/apiserver-kubelet-client.crt --key /etc/kubernetes/pki/apiserver-kubelet-client.key
{"items":["/var/lib/kubelet/checkpoints/checkpoint-mem-dummy-deployment-66db99f88f-fzb22_default-mem-dummy-2024-03-13T16:22:03Z.tar"]}
real	0m5.868s
user	0m0.013s
sys	0m0.000s
root@master-3:~# kubectl top pods
NAME                                    CPU(cores)   MEMORY(bytes)   
mem-dummy-deployment-66db99f88f-fzb22   0m           746Mi 

#### checkpoint mem-dummy:

1. vm spec:
   1. 1 vCore, 2GiB of RAM
2. pod util:
   1. CPU:0m; RAM:746Mi
3. time for checkpoint (time <the checkpoint curl command...>)
   1. real	1m49.125s
      user	0m0.008s
      sys	0m0.008s

#### resore mem-dummy:

1. vm spec:
   1. 1 vCore, 2GiB of RAM
2. time for transfer
   1. 
3. time for transfer
   1. local nodes
      1. 
   2. neighbor clusers
      1. limit: in/out - 1000Mbit, 100ms
         1. 
      2. limit: in/out - 1000Mbit, 50ms
         1. 
      3. limit: in/out - 100Mbit, 100ms
         1. 
      4. limit: in/out - 100Mbit, 50ms
         1. 