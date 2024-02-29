# notes

## in-yaml change
1. priority classes
   1. label based on application type
2. node/pod affnity
   1. HA? replica? bundled applications?

## custom sched
deprecated in ?v1.16

## sched framework
1. Predicates - stage filter --might not change much
   1. PodFitsResources
   2. PodFitsHostPorts
   3. PodMatchNodeSelector
   4. NoDiskConflict
   5. CheckNodeDiskPressure
   6. CheckNodeMemoryPressure
   7. CheckNodeCondition
   8. !!! apply filter on hard network status limitor

2. Priorities - stage rank -- major change to sorting section of best rank
   1. determine if HA or replica needed
   2. -> best-fit approach, but based on spec. requirements, network readings priority > resource
   3. examine if needed to skip the queue
