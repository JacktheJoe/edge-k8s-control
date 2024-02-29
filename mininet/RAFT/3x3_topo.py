from mininet.net import Mininet
from mininet.node import Controller, OVSSwitch
from mininet.node import Host
from mininet.topo import Topo
from mininet.link import Link
from mininet.cli import CLI
from mininet.log import setLogLevel, info

class GridTopo(Topo):
    def build(self):
        # Add a switch
        switch = self.addSwitch('s1')

        # Add hosts with specific IP addresses
        hosts = []
        for i in range(1, 10):
            host = self.addHost('h%d' % i, ip='10.0.0.%d' % i)
            hosts.append(host)

        # Connect hosts to the switch
        for host in hosts:
            self.addLink(host, switch)

def run():
    topo = GridTopo()
    net = Mininet(topo=topo, host=Host, link=Link, controller=Controller, switch=OVSSwitch)

    net.start()

    # Open xterm windows for h1 to h9 and run the script
    for i in range(1, 10):
        host = net['h{}'.format(i)]
        host.cmd('xterm -e "bash -c \'/home/jack/Desktop/mininet/RAFT-like/node.sh; exec bash\'" &')

    # Open CLI for manual testing
    CLI(net)

    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    run()
