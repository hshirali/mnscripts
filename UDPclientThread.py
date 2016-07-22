import socket
import sys, getopt
import time
from threading import Thread

def UDPclient(UDP_IP, UDP_PORT, total,result,index,loglevel=None):
    time1 = time.time()
    t1=time1
    count = 0
    error = 0
    #    wait=0.005 # in ms
    for i in range(0, total, 1):
        try:
            #time.sleep(20000/1000)
            MESSAGE = "Hello, World!"
            sock = socket.socket(socket.AF_INET,  # Internet
                                 socket.SOCK_DGRAM)  # UDP
            sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))
            count = count + 1
            if loglevel=='log':
                if i%10000 == 0 :
                    t2=time.time()
                    print "at %i \t %0.3f ms" % (i,(t2-t1)*1000)
                    t1=t2
        except:
            error = error + 1
            print 'erro'

    time2 = time.time()
    #print "total",total,"\t index " ,index
    result[index] =(time2 - time1)  #{'time':(time2 - time1),'count':count,'error':error}



UDP_IP = "127.0.0.1"
UDP_PORT = 5005
MESSAGE = "Hello, World!"

totalmessage=10;
threadnum=1
loglevel=None

argv=sys.argv[1:]
try:
    opts, args = getopt.getopt(argv, "hi:p:c:t:l:", ["ip=", "port=","count=","loglevel="])
except getopt.GetoptError:
    print 'TCPclient.py -i <ip> -p <port>'
    sys.exit(2)
for opt, arg in opts:
    if opt == '-h':
        print 'TCPclient.py -i <ip> -o <port>'
        sys.exit()
    elif opt in ("-i", "--ip"):
        UDP_IP = arg
    elif opt in ("-p", "--port"):
        UDP_PORT = int(arg)
    elif opt in ("-c", "--count"):
        totalmessage=int(arg)
    elif opt in ("-t", "--thread"):
        threadnum= int(arg)
    elif opt in ("-l", "--thread"):
        loglevel=arg

print "UDP target IP:", UDP_IP
print "UDP target port:", UDP_PORT
print "message:", MESSAGE
print "thread:",threadnum
print "count:",totalmessage
print loglevel
threads = [None] * threadnum
results = [None] * threadnum

time1m = time.time()

for i in range(len(threads)):
    threads[i] = Thread(target=UDPclient, args=(UDP_IP,UDP_PORT,totalmessage/threadnum ,results,i,loglevel))
    threads[i].start()

for i in range(len(threads)):
    threads[i].join()
time2m = time.time()

#res=results[0]
difftime=time2m-time1m
difftime=sum(results)/threadnum
#difftime=result['time']
#count=result['count']
count=totalmessage

print ('%i connect took %0.3f ms\n each connection take  %0.3f ms \n each connection take  %0.3f micros\n %i pers second' % (
        count, difftime * 1000.0, difftime * 1000.0 / count, difftime * 1000 * 1000 / count,int(count/difftime)))



