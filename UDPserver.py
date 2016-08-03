import socket
import sys, getopt
import time
from threading import Thread
import multiprocessing

def UDPserver(UDP_IP, UDP_PORT,loglevel=None):

    sock = socket.socket(socket.AF_INET, # Internet
                         socket.SOCK_DGRAM) # UDP
    sock.bind((UDP_IP, UDP_PORT))
    count =0
    if loglevel == 'log':
        print "start server %s  port %s" % (UDP_IP ,UDP_PORT )
    start=time.time()
    sock.settimeout(1)
    lastprint = end=start
    data='*Null*'
    try:
        while True:
            data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
            end=time.time()
            count = count + 1
            if loglevel == 'log' :
                if time.time()-lastprint>.2:
                #if count % 20000 == 0 :
                    print "%i received message:" % (count), data
                    lastprint=time.time()
    except:
        if loglevel == 'log' or loglevel == 'debug':
            #print("Unexpected error:", sys.exc_info()[0])
            print "%i received message: %s" % ((count), data)
        if loglevel == 'log':
            print "time in server %3f " % (end-start)
            print "all time %.3f" % (time.time()-start)

def TcpThread(s):

    lastprint = end=start=time.time()
    timeout = 1.0

    count=0
    data = '*Null*'
    tout=1
    while 1:
        try:
            st1 = time.time()
            conn, addr = s.accept()

            if tout and 0:
                tout=0
                s.settimeout(200.0/1000)
            BUFFER_SIZE = 60  # Normally 1024, but we want fast response

            while 0:
                data = conn.recv(BUFFER_SIZE)
                if not data: break
                #conn.send(data)
            st3 = time.time()
            conn.shutdown(socket.SHUT_RDWR)
            st4 = time.time()
            conn.close()
            end=time.time()
            if (end - st1) * 1000 > 100 and 1:
                print '^^^^^^^^^^^^^^^^^^^^^^^^^ %i: \tst1:%.1f\tst3:%.1f\tst4:%.1f' % (
                    count, (end - st1) * 1000, (end - st3) * 1000,
                    (end - st4) * 1000)
        except socket.timeout:

            tout=1
            gettim=s.gettimeout()

            if gettim<timeout/2:
                s.settimeout(gettim*2)
            elif gettim<timeout:
                s.settimeout(timeout)
            else:
                print 'timeout:', gettim
                break
        except socket.error, e:
            print 'error Thread:\t%s' % ( e)
            break
        except:
            if loglevel == 'log' or loglevel == 'debug':
                print("Unexpected error:", sys.exc_info()[0])
                print "%i received message: %s" % ((count), data)
            break
    if loglevel == 'log':

        print "time in server %1f ms" % ((end - start) * 1000)
        print "all time %.3f" % (time.time() - start)


def TCPserver(TCP_IP, TCP_PORT,loglevel=None):
    try:
        threadnum=5
        timeout=3.0
        threads = [None] * threadnum

        for i in range(len(threads)):
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
            s.bind((TCP_IP, TCP_PORT))
            lastprint = end = start = time.time()
            s.listen(10)
            s.settimeout(timeout)

            threads[i] =Thread(target=TcpThread, args=(s,))
            threads[i].start()

        for i in range(len(threads)):
            threads[i].join()
    except socket.error, e:
        print 'error Main %i:\t%s' % (i, e)
    except:
        if loglevel == 'log' or loglevel == 'debug':
            print("Unexpected error:", sys.exc_info()[0])

Target_IP = "127.0.0.1"
Target_PORT = 5005
loglevel=None
protocol=None
argv=sys.argv[1:]

try:
    opts, args = getopt.getopt(argv, "hi:p:l:y:", ["ip=", "port=","loglevel=","protocol="])
except getopt.GetoptError:
    print 'serverside.py -i <ip bind> -p <port bind> -l loglevel -y protocol'
    sys.exit(2)
for opt, arg in opts:
    if opt == '-h':
        print 'clientside.py -i <ip> -o <port>'
        sys.exit()
    elif opt in ("-i", "--ip"):
        Target_IP = arg
    elif opt in ("-p", "--port"):
        Target_PORT = int(arg)
    elif opt in ("-l", "--loglevel"):
        loglevel = arg
    elif opt in ("-y", "--protocol"):
        protocol = arg
if protocol =='udp':
    UDPserver(Target_IP, Target_PORT, loglevel)
elif protocol=='tcp':
    TCPserver(Target_IP, Target_PORT, loglevel)
else : print 'Error in protocol:',protocol