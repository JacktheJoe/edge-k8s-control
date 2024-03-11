learned the hard way:

1. if the original setup is root then use root
2. priviliage for crt and key
3. always pre-define the varibales, update them or store locally and fill-in-blank
4. retrive from worker node where is deployed


test results for checkpointing and restoring the counter pod, with scp and local rebuilds (no public/private reg)
result for checkpoint on cluster-2 (org w-2)
1. restore on cluster-2
   1. w-2
      1. passed
   2. w-1
      1. passed
2. restore on cluster-3
   1. w-2
      1. passed
   2. w-1
      1. passed

result for checkpoint on cluster-3 (org w-2)
1. restore on cluster-3
   1. w-2
      1. passed
   2. w-1
      1. passed
2. restore on cluster-2
   1. w-2
      1. passed
   2. w-1
      1. passed

solution -> but futher problems for check pointing: 
1. need to send the original checkpoint tarball and/or construct Dockerfile to dest node