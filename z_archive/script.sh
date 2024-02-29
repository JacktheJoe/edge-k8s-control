

sudo swapon --show

wget https://github.com/containerd/containerd/releases/download/v1.6.24/containerd-1.6.24-linux-amd64.tar.gz

sudo tar Cxzvf /usr/local containerd-1.6.24-linux-amd64.tar.gz

wget https://raw.githubusercontent.com/containerd/containerd/main/containerd.service

sudo mv containerd.service /usr/lib/systemd/system/

sudo systemctl daemon-reload

sudo systemctl enable --now containerd

sudo systemctl status containerd

wget https://github.com/opencontainers/runc/releases/download/v1.1.9/runc.amd64

sudo install -m 755 runc.amd64 /usr/local/sbin/runc

sudo mkdir -p /etc/containerd/

containerd config default | sudo tee /etc/containerd/config.toml

sudo sed -i 's/SystemdCgroup \= false/SystemdCgroup \= true/g' /etc/containerd/config.toml

sudo systemctl restart containerd

wget https://github.com/containernetworking/plugins/releases/download/v1.3.0/cni-plugins-linux-amd64-v1.3.0.tgz

sudo mkdir -p /opt/cni/bin

sudo tar Cxzvf /opt/cni/bin/ cni-plugins-linux-amd64-v1.3.0.tgz

curl -s https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo gpg --dearmour -o /etc/apt/trusted.gpg.d/kubernetes-xenial.gpg

sudo apt-add-repository "deb http://apt.kubernetes.io/ kubernetes-xenial main"

sudo apt update

sudo apt install -y kubelet kubeadm kubectl

sudo apt-mark hold kubelet kubeadm kubectl

sudo nano /proc/sys/net/ipv4/ip_forward

cat <<EOF | sudo tee /etc/modules-load.d/k8s.conf
overlay
br_netfilter
EOF

sudo modprobe overlay

sudo modprobe br_netfilter

cat <<EOF | sudo tee /etc/sysctl.d/k8s.conf
net.bridge.bridge-nf-call-iptables  = 1
net.bridge.bridge-nf-call-ip6tables = 1
net.ipv4.ip_forward                 = 1
EOF

sudo sysctl --system

lsmod | grep br_netfilter

lsmod | grep overlay

sysctl net.bridge.bridge-nf-call-iptables net.bridge.bridge-nf-call-ip6tables net.ipv4.ip_forward

