apt install apt-transport-https ca-certificates curl software-properties-common

curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -

add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu focal stable"

apt install docker-ce -y

systemctl restart docker

inside /etc/docker/registry/config.yml

version: 0.1
log:
  level: info
  formatter: json
  fields:
    service: registry
storage:
  cache:
    layerinfo: inmemory
  filesystem:
    rootdirectory: /var/lib/registry
http:
  addr: :5000
  tls:
    certificate: /certs/domain.crt
    key: /certs/domain.key

inside /etc/docker/daemon.json

{
  "insecure-registries": ["node's IP:5000"]
}

systemctl restart docker

then, docker command:

docker container run -d -p 5000:5000 -v REGISTRY_STORAGE_DELETE_ENABLED=true --name registry_basic registry

img in docker 

curl 127.0.0.1:5000/v2/_catalog

in crio/config.yaml

insecure_registries = [
  "10.100.25.10/24"
]

registries = [
  "10.100.25.10:5000",
  "docker.io"
]
