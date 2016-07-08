#!/usr/bin/env python

import sys

from mininet.topo import Topo
from mininet.cli import CLI
from mininet.net import Mininet
from mininet.node import RemoteController, OVSKernelSwitch
from mininet.log import setLogLevel

class TowerTopo( Topo ):
    """Create a tower topology"""

    def build( self, k=20, h=2 ):
        spines = []
        leaves = []
        hosts = []

        # Create the two spine switches
        spines.append(self.addSwitch('s1'))
        spines.append(self.addSwitch('s2'))

        # Create two links between the spine switches
        self.addLink(spines[0], spines[1])
        #TODO add second link between spines when multi-link topos are supported
        #self.addLink(spines[0], spines[1])
        
        # Now create the leaf switches, their hosts and connect them together
        i = 1
        c = 0
        while i <= k:
            leaves.append(self.addSwitch('s1%d' % i))
            for spine in spines:
                self.addLink(leaves[i-1], spine)

            j = 1
            while j <= h:
                hosts.append(self.addHost('h%d%d' % (i, j)))
                self.addLink(hosts[c], leaves[i-1])
                j+=1
                c+=1

            i+=1

topos = { 'tower': TowerTopo }

def run( controllers ):
    topo = TowerTopo()
    net = Mininet( topo=topo, controller=None, autoSetMacs=True )
    ctrl_count = 0
    for controllerIP in controllers:
        net.addController( 'c%d' % ctrl_count, RemoteController, ip=controllerIP )
        ctrl_count += 1
    net.start()
    CLI( net )
    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    if len( sys.argv ) > 1:
        controllers = sys.argv[ 1: ]
    else:
        print 'Usage: startnet <c0 IP> <c1 IP> ...'
        exit( 1 )
    run( controllers )

