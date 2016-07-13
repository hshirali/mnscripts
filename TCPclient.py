#!/usr/bin/env python

import socket
import sys, getopt
import time

TCP_IP = '127.0.0.1'
TCP_PORT = 5005

argv=sys.argv[1:]
try:
    opts, args = getopt.getopt(argv, "hi:p:", ["ip=", "port="])
except getopt.GetoptError:
    print 'TCPclient.py -i <ip> -p <port>'
    sys.exit(2)
for opt, arg in opts:
    if opt == '-h':
        print 'TCPclient.py -i <ip> -o <port>'
        sys.exit()
    elif opt in ("-i", "--ip"):
        TCP_IP = arg
    elif opt in ("-p", "--port"):
        TCP_PORT = int(arg)

time1 = time.time()
count =0
error =0
wait=0.00005
for i in range(0,100,1):
    try:
        BUFFER_SIZE = 1024
        MESSAGE = "Hello, World!"
        time.sleep(wait)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((TCP_IP, TCP_PORT))
        s.send(MESSAGE)
        #data = s.recv(BUFFER_SIZE)
        s.close()
        count = count + 1
    except:
        error=error+1

    #print "received data:", data
time2 = time.time()
print ('%i connect took %0.3f ms \n wated %0.3f ms' % (count,(time2 - time1) * 1000.0,wait*1000))