curl -X POST "https://nodeIP:10250/checkpoint/namespace/podID/container" --insecure --cert /etc/kubernetes/pki/apiserver-kubelet-client.crt --key /etc/kubernetes/pki/apiserver-kubelet-client.key

for buildah and policy: (over-write needed + allow access)

sudo apt-get -o Dpkg::Options::="--force-overwrite" install buildah -y

cd /etc/kubernetes/pki/ && chmod 777 ./*



NODEIP="10.200.35.12"

NS=default

PODID=counter-deployment-ddbdd9dd6-vgts6

CONTAINER=counter

curl -X POST "https://$NODEIP:10250/checkpoint/$NS/$PODID/$CONTAINER" --insecure --cert /etc/kubernetes/pki/apiserver-kubelet-client.crt --key /etc/kubernetes/pki/apiserver-kubelet-client.key

{"items":["/var/lib/kubelet/checkpoints/checkpoint-counter-deployment-ddbdd9dd6-m59ds_default-counter-2024-02-29T18:28:17Z.tar"]}


newcontainer=$(build from scratch)

buildah add $newcontainer /var/lib/kubelet/checkpoints/



commands used for checkpointing:
 - curl -X POST "https://nodeIP:10250/checkpoint/namespace/podID/container" --insecure --cert /etc/kubernetes/pki/apiserver-kubelet-client.crt --key /etc/kubernetes/pki/apiserver-kubelet-client.key
 - for example, under default, deployment job name = counter-deployment, pod name = counter-deployment-ddbdd9dd6-jddlv, node = cluster1_worker2,
   - command will be:
     - curl -X POST "https://10.100.21.22:10250/checkpoint/default/counter-deployment-ddbdd9dd6-jddlv/counter" --insecure --cert /etc/kubernetes/pki/apiserver-kubelet-client.crt --key /etc/kubernetes/pki/apiserver-kubelet-client.key

size fetching and comparison
  1. commands used to fetch image in k8s and list size in M:
      1. kubectl get nodes -o json | jq '.items[].status.images[] | .names[1], (.sizeBytes | tonumber/1024/1024)'
         1. "docker.io/xz446/criu-test-counter:0.1"   (because of the use of python 3.9, which is massive)
            972.1451969146729
  2. compare to dh -h ./checkpoint_name to see incremental size difference
      1. 4.5M	./check1.tar  (just a simple python program that counts)

!! no fixes for package conflicts. migratinig all cluster systems to ubuntu 20.04 instead

new setup: after critical ssd sector failure:
    1. pfsense + ubuntu -> wireless to linux bridge && subnets for management & all other interfaces
    2. proxmox on debian 12 desktop -> for local management and critical failure recovery and off-line management
    3. truenas + passthrough mirrored p31 -> raid 1 to prevent ssd failure from destroying all vms && dedicate eth interface between proxmox and truenas for nfs storage

tested with buildah install:
    1. ubuntu 22.04: broken, dependency conflicts
    2. ubuntu 20.04: was able to install without any issue.......
       1. ! the kernel needed to be upgrade to at least 5.9, I did 5.15 because of CRIU requirements
       2. but after such checkpoint and restore finally worked
       3. using latest hwe kernel (seemed) solved the bpfilter (fw) read fail 0 problem, version 5.15.0-100-generic

image layer location in k8s: 
    1. buildah compiled image under target node's -> /var/lib/containers/storage/overlay-images
    2. buildah compiled image's layers possibly under -> /var/lib/containers/storage/overlay
    3. seems kubernetes pulled layers stored under -> /var/run/containers/storage/overlay-containers or similar dirs

    trying to see how to only apply/swap cached/changed layers to target, or for common applications, based on &*&$ algorithm migrate them to dest of dir


DOCKER_RATE_LIMIT (100-200/6hrs)

to check (no log-in):
1. TOKEN=$(curl "https://auth.docker.io/token?service=registry.docker.io&scope=repository:ratelimitpreview/test:pull" | jq -r .token)
2. curl --head -H "Authorization: Bearer $TOKEN" https://registry-1.docker.io/v2/ratelimitpreview/test/manifests/latest

if no remaining then limit reach and image pull will never work