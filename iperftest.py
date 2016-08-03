#!/usr/bin/python

import time

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import CPULimitedHost
from mininet.link import TCLink
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel
from mininet.cli import CLI

from mininet.log import info, error, debug, output, warn
from mininet.util import (quietRun, fixLimits, numCores, ensureRoot,
                          macColonHex, ipStr, ipParse, netParse, ipAdd,
                          waitListening)


class SingleSwitchTopo(Topo):
    "Single switch connected to n hosts."
    def build(self, n=2):
        switch = self.addSwitch('s1')
        for h in range(n):
            # Each host gets 50%/n of system CPU
            host = self.addHost('h%s' % (h + 1),
               cpu=.5/n)
            # 10 Mbps, 5ms delay, 10% loss, 1000 packet queue
            self.addLink(host, switch,
               )

def timing(f):
    def wrap(*args):
        time1 = time.time()
        ret = f(*args)
        time2 = time.time()
        output('%s function took %0.3f ms' % (f.func_name, (time2-time1)*1000.0))
        return ret
    return wrap

@timing
def myiperf(self, hosts=None, l4Type='TCP', udpBw='10M', fmt=None,
          seconds=2, port=5001):
    """Run iperf between two hosts.
       hosts: list of hosts; if None, uses first and last hosts
       l4Type: string, one of [ TCP, UDP ]
       udpBw: bandwidth target for UDP test
       fmt: iperf format argument if any
       seconds: iperf time to transmit
       port: iperf port
       returns: two-element array of [ server, client ] speeds
       note: send() is buffered, so client rate can be much higher than
       the actual transmission rate; on an unloaded system, server
       rate should be much closer to the actual receive rate"""


    hosts = hosts or [self.hosts[0], self.hosts[-1]]
    assert len(hosts) == 2
    client, server = hosts
    output('*** Iperf: testing', l4Type, 'bandwidth between',
           client, 'and', server, '\n')
    server.cmd('killall -9 iperf')
    iperfArgs = 'iperf3 -p %d ' % port
    bwArgs = ''
    if l4Type == 'UDP':
        iperfArgs += '-u '
        bwArgs = '-b ' + udpBw + ' '
    elif l4Type != 'TCP':
        raise Exception('Unexpected l4 type: %s' % l4Type)
    if fmt:
        iperfArgs += '-f %s ' % fmt
    server.sendCmd(iperfArgs + '-s')
    if l4Type == 'TCP':
        if not waitListening(client, server.IP(), port):
            raise Exception('Could not connect to iperf on port %d'
                            % port)
    time1 = time.time()
    ttt=2
    for coun in range(3):
        cliout = client.cmd(iperfArgs + '-P 20 -l 42 -n %d -c ' % ttt +
                        server.IP() + ' ' + bwArgs)
#        time.sleep(.01)
    time2 = time.time()
    output('this took %0.3f ms \n' % ( (time2 - time1) * 1000.0))

    debug('Client output: %s\n' % cliout)
    server.sendInt()
    servout = server.waitOutput()
    debug('Server output: %s\n' % servout)
    result = [self._parseIperf(servout), self._parseIperf(cliout)]
    if l4Type == 'UDP':
        result.insert(0, udpBw)
    output('*** Results: %s\n' % result)
    return result


def perfTest():
    "Create network and run simple performance test"
    topo = SingleSwitchTopo(n=4)
    net = Mininet(topo=topo,
                  host=CPULimitedHost, link=TCLink)

    net.start()
    print "Dumping host connections"
    dumpNodeConnections(net.hosts)
    print "Testing network connectivity"
    #net.pingAll()
    print "Testing bandwidth between h1 and h4"
    h1, h4 = net.get('h1', 'h4')
    CLI(net)
    myiperf(net,(h1, h4))
    CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    perfTest()
