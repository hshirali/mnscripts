#!/usr/bin/env python

import sys

from mininet.topo import Topo
from mininet.cli import CLI
from mininet.net import Mininet
from mininet.node import RemoteController, OVSKernelSwitch
from mininet.log import setLogLevel
import time
from threading import Thread
from myTree import TreeNet
from mininet.log import info, error, debug, output
import multiprocessing


def sendudp(self, hosts=None, number=10, numberpersecond=0):
    hosts = hosts or [self.hosts[0], self.hosts[-1]]
    assert len(hosts) == 2
    client, server = hosts
    ServerOutput = ""
    cliout=''
    protocol='tcp'
    if protocol =='udp':
        print "send %i packet from %s to %s" % (number,client,server)

        udpservercommand = 'python UDPserver.py --ip=%s --log=log --protocol=%s' % (
            server.IP(),'udp')

        if udpservercommand != None:
            server.sendCmd(udpservercommand)

        udpcommand = 'python clientside.py -c %i -t %i -i %s -l debug -n %i -y %s' % (
            number, min(int(number / 10000) + 1, 10), server.IP(),numberpersecond,'udp')
        cliout = client.cmd(udpcommand)

        if udpservercommand != None:
            t = time.time()
            t2 = t
            start = t
            ServerOutput = server.monitor(timeoutms=200)

            while server.waiting and time.time() - t < 5:
                if t2 + .3 < time.time():
                    t2 = time.time()
                    Output = server.monitor(2)
                    ServerOutput+=Output
                    if len(Output) != 0:
                        t = time.time()

            server.sendInt()
            ServerOutput += server.waitOutput()
    if protocol == 'tcp':
        tcpservercommand = 'python UDPserver.py --ip=%s --log=log --protocol=%s' % (
            server.IP(),'tcp')
        if tcpservercommand != None:
            server.sendCmd(tcpservercommand)

        tcpcommand = 'python clientside.py --count=%i --process=%i --ip=%s --loglevel=log --numberpersecond=%i --protocol=%s' % (
            number, min(int(number / 100) + 1, 5), server.IP(), numberpersecond, 'tcp')
        cliout = client.cmd(tcpcommand)
        t = time.time()
        t2 = t
        start = t
        ServerOutput = server.monitor(timeoutms=200)

        while server.waiting and time.time() - start < 5:
            if t2 + .3 < time.time():
                t2 = time.time()
                Output = server.monitor(2)
                ServerOutput += Output
                if len(Output) != 0:
                    t = time.time()

        server.sendInt()
        ServerOutput += server.waitOutput()

    print('************Client %s output**********:\n %s' % (client.IP(), cliout))

    print('************Server %s output**********:\n %s' % (server.IP(), ServerOutput))


def run(controllers):
    # net = Mininet( topo=topo, controller=None, autoSetMacs=True )
    net = TreeNet(depth=2, fanout=4, controller=None)
    ctrl_count = 01
    for controllerIP in controllers:
        net.addController('c%d' % ctrl_count, RemoteController, ip=controllerIP)
        ctrl_count += 1
    net.start()
    #net.pingAll(1000)
    # CLI(net)

    threads = []
    threads.append(Thread(target=sendudp, args=(net, net.get('h1', 'h2'), 1000,1000)))
    #threads.append(Thread(target=sendudp, args=(net, net.get('h3', 'h4'), 8000,000)))
    #threads.append(Thread(target=sendudp, args=(net, net.get('h5', 'h6'), 7000, 000)))
    #threads.append(Thread(target=sendudp, args=(net, net.get('h7', 'h8'), 6000, 000)))
    #threads.append(Thread(target=sendudp, args=(net, net.get('h9', 'h10'), 9000, 000)))

    for i in range(len(threads)):
        threads[i].start()

    for i in range(len(threads)):
        threads[i].join()

    # CLI( net )
    net.stop()

if __name__ == '__main__':
    #setLogLevel('info')

    if len(sys.argv) > 1:
        controllers = sys.argv[1:]
    else:
        print 'Usage: startnet <c0 IP> <c1 IP> ...'
        exit(1)
    run(controllers)
