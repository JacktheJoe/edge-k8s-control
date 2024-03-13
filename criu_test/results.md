## results for checkpointing:

### for container mem-dummy:
Mem-dummy just holds a lot of ram, for example, current config is about 1GiB of ram. 
meaningless, but a good thing to test relative performance

#### checkpoint mem-dummy:

1. vm spec:
   1. 1 vCore, 2GiB of RAM
2. pod util:
   1. CPU:0m; RAM:1488Mi
3. time for checkpoint (time <the checkpoint curl command...>)
   1. real	1m49.125s
      user	0m0.008s
      sys	0m0.008s

#### resore mem-dummy:

1. vm spec:
   1. 1 vCore, 2GiB of RAM
2. time for transfer
   1. 
3. time for restore
   1. local nodes (limit ~10G -> native)
      1. 
   2. neighbor clusers (limit ~gigabit, ~100M, ~10M with different latency and gitter)
      1. 