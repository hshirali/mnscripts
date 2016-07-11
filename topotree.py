#!/usr/bin/env python

import sys

from mininet.topo import Topo
from mininet.cli import CLI
from mininet.net import Mininet
from mininet.node import RemoteController, OVSKernelSwitch
from mininet.log import setLogLevel
#from mininet.topolib import TreeNet
from myTree import TreeNet

def run( controllers ):
   # net = Mininet( topo=topo, controller=None, autoSetMacs=True )
    net = TreeNet( depth=1, fanout=3, controller=None)
    ctrl_count = 01
    for controllerIP in controllers:
        net.addController( 'c%d' % ctrl_count, RemoteController, ip=controllerIP )
        ctrl_count += 1
    net.start()
    #CLI( net )

    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    if len( sys.argv ) > 1:
        controllers = sys.argv[ 1: ]
    else:
        print 'Usage: startnet <c0 IP> <c1 IP> ...'
        exit( 1 )
    run( controllers )

