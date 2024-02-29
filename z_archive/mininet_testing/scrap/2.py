from mininet.net import Mininet
from mininet.node import Host
from mininet.topo import Topo
from mininet.link import Link
from mininet.cli import CLI
from mininet.log import setLogLevel, info
import time

class GridTopo(Topo):
    def build(self):
        # Create 9 hosts
        h1 = self.addHost('h1', ip='10.0.0.1/24')
        h2 = self.addHost('h2', ip='10.0.0.2/24')
        h3 = self.addHost('h3', ip='10.0.0.3/24')
        h4 = self.addHost('h4', ip='10.0.0.4/24')
        h5 = self.addHost('h5', ip='10.0.0.5/24')
        h6 = self.addHost('h6', ip='10.0.0.6/24')
        h7 = self.addHost('h7', ip='10.0.0.7/24')
        h8 = self.addHost('h8', ip='10.0.0.8/24')
        h9 = self.addHost('h9', ip='10.0.0.9/24')

        # Add links between hosts
        self.addLink(h1, h2)
        self.addLink(h1, h4)
        self.addLink(h2, h3)
        self.addLink(h2, h5)
        self.addLink(h3, h6)
        self.addLink(h4, h5)
        self.addLink(h4, h7)
        self.addLink(h5, h6)
        self.addLink(h5, h8)
        self.addLink(h6, h9)
        self.addLink(h7, h8)
        self.addLink(h8, h9)

def run():
    topo = GridTopo()
    net = Mininet(topo=topo, host=Host, link=Link, controller=None)

    info(net['h1'].cmd('ip route add 10.0.0.4/32 dev h1-eth1'))
    info(net['h1'].cmd('ip route add 10.0.0.2/32 dev h1-eth0'))

    info(net['h2'].cmd('ip route add 10.0.0.1/32 dev h2-eth0'))
    info(net['h2'].cmd('ip route add 10.0.0.3/32 dev h2-eth1'))
    info(net['h2'].cmd('ip route add 10.0.0.5/32 dev h2-eth2'))

    info(net['h3'].cmd('ip route add 10.0.0.2/32 dev h3-eth0'))
    info(net['h3'].cmd('ip route add 10.0.0.6/32 dev h3-eth1'))

    info(net['h4'].cmd('ip route add 10.0.0.1/32 dev h4-eth0'))
    info(net['h4'].cmd('ip route add 10.0.0.5/32 dev h4-eth1'))
    info(net['h4'].cmd('ip route add 10.0.0.7/32 dev h4-eth2'))

    info(net['h5'].cmd('ip route add 10.0.0.2/32 dev h5-eth0'))
    info(net['h5'].cmd('ip route add 10.0.0.4/32 dev h5-eth1'))
    info(net['h5'].cmd('ip route add 10.0.0.6/32 dev h5-eth2'))
    info(net['h5'].cmd('ip route add 10.0.0.8/32 dev h5-eth3'))

    info(net['h6'].cmd('ip route add 10.0.0.3/32 dev h6-eth0'))
    info(net['h6'].cmd('ip route add 10.0.0.5/32 dev h6-eth1'))
    info(net['h6'].cmd('ip route add 10.0.0.9/32 dev h6-eth2'))

    info(net['h7'].cmd('ip route add 10.0.0.4/32 dev h7-eth0'))
    info(net['h7'].cmd('ip route add 10.0.0.8/32 dev h7-eth1'))

    info(net['h8'].cmd('ip route add 10.0.0.5/32 dev h8-eth0'))
    info(net['h8'].cmd('ip route add 10.0.0.7/32 dev h8-eth1'))
    info(net['h8'].cmd('ip route add 10.0.0.9/32 dev h8-eth2'))
    
    info(net['h9'].cmd('ip route add 10.0.0.6/32 dev h9-eth0'))
    info(net['h9'].cmd('ip route add 10.0.0.8/32 dev h9-eth1'))

    net.start()

    # Open xterm windows for h1 to h9 and run the script
    for i in range(1, 10):
        host = net['h{}'.format(i)]
        host.cmd('xterm -e "bash -c \'/home/jack/Desktop/mininet/3x3/node.sh; exec bash\'" &')

    # Open CLI for manual testing
    CLI(net)

    net.stop()

topos = {'test': (lambda: GridTopo())}

if __name__ == '__main__':
    setLogLevel('info')
    run()
