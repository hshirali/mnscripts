import socket
import sys, getopt
import time
from threading import Thread
import multiprocessing
import errno

def clientfun(Target_IP, Target_PORT, total, index, loglevel=None, NumberPerSecond=10000, protocol='udp'):

    spendtime=0
    Next=time1 = time.time()
    error = 0
    #wait = 10.0/1000/1000
    #state=0
    count =0
    c2=0
    tm=0
    tt=0
    tt2=0
    tt3=0

    for i in range(0, total, 1):
        try:
            MESSAGE = "Hello, World! %i" % i
            if protocol =='udp':
                sock = socket.socket(socket.AF_INET,  # Internet
                                     socket.SOCK_DGRAM)  # UDP
                sock.sendto(MESSAGE, (Target_IP, Target_PORT))
            elif protocol =='tcp':

                st1=time.time()
                #state=1
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
                s.settimeout(1500.0/1000)
                #state =2
                #st2=time.time()
                s.connect((Target_IP, Target_PORT))


                #state =3

                #s.send(MESSAGE)
                #data = s.recv(30)
                #time.sleep(wait)
                #state =4
                #st3 = time.time()
                s.shutdown(socket.SHUT_RDWR)

                #st4 = time.time()
                s.close()
                count +=1

                #time.sleep(wait)
                dur=time.time()-st1
                if dur*1000>200:
                    print '^^^^^^^^^^^^^^^^^^^^^^^^^in %i : %i \tst1:%.1f' % (index,i,(time.time()-st1)*1000)
                    #,(time.time()-st2)*1000,(time.time()-st3)*1000,(time.time()-st4)*1000)
                #else :
                    #arrtimes.append(time.time() - st1)
                    #arrtimes2.append(time.time()-st2)
            else :
                return

            if NumberPerSecond>0:

                end=time.time()
                dur=(end-Next)
                tm=max(dur,tm)
                spendtime += 1/float(NumberPerSecond) - dur -3.0/1000/1000
                tt2+=dur
                #tt+=1/float(NumberPerSecond)- dur

                #print 'duration',duration
                if spendtime>0:
                    tt+=spendtime
                    time.sleep(spendtime)
                    spendtime-=(time.time() - end)
                    c2+=1

                if count % NumberPerSecond==0 and loglevel=='log':
                    print count,"\t",(time.time() - time1)*1000
                tt3 += (time.time() - end)
                Next = time.time()
        except socket.timeout:
            #print 'timeout'
            error +=1
        except socket.error, e:
            print 'error:%s\t%s' % (0,e)

    time2 = time.time()

    if loglevel == 'log' and 1:
        print "in proccess %i at %i \t %0.3f ms  per flow\t %0.3f microsec" % (
            index,count, (time2 - time1) * 1000,(time2 - time1)/total*1000*1000)
        #print 'spend',spendtime
        #print 'tt',(tt*1000)
        #print 'tm', (tm * 1000)
        #print 'tt2', (tt2 * 1000*1000/count)
        #print 'tt3', (tt3 * 1000)
        #print 'c2',c2
    if error>0 :
        print 'have %i timeout' % error

Target_IP = "127.0.0.1"
Target_PORT = 5005
MESSAGE = "Hello, World!"

TotalMessage=10;
ProcessNumber=1
LogLevel=None
NumberPerSecond=1
argv=sys.argv[1:]
protocol='tcp'
try:
    opts, args = getopt.getopt(argv, "hi:p:c:t:l:n:y:", ["ip=", "port=","count=","process=","loglevel="
        ,"numberpersecond=","protocol="])
except getopt.GetoptError:
    print 'clientside.py -i <ip> -p <port>'
    sys.exit(2)
for opt, arg in opts:
    if opt == '-h':
        print 'clientside.py -i <ip> -o <port>'
        sys.exit()
    elif opt in ("-i", "--ip"):
        Target_IP = arg
    elif opt in ("-p", "--port"):
        Target_PORT = int(arg)
    elif opt in ("-c", "--count"):
        TotalMessage=int(arg)
    elif opt in ("-t", "--process"):
        ProcessNumber= int(arg)
    elif opt in ("-l", "--loglevel"):
        LogLevel=arg
    elif opt in ("-n", "--numberpersecond"):
        NumberPerSecond = int(arg)
    elif opt in ("-y", "--protocol"):
        protocol = arg.lower()
        if protocol!='tcp' and protocol!='udp':
            print 'protocol tcp or udp'
            sys.exit()
if LogLevel== 'log':
    print "UDP target IP:", Target_IP
    print "UDP target port:", Target_PORT
    print "message client:", MESSAGE
    print "process:",ProcessNumber
    print "count:",TotalMessage
    print LogLevel
    print "number per second" ,NumberPerSecond
    print "protocol: ", protocol

ProccessArray = [None] * ProcessNumber

time1m = time.time()

for i in range(len(ProccessArray)):
    #ProccessArray[i] = multiprocessing.Process(target=clientfun, args=(
    ProccessArray[i] = multiprocessing.Process(target=clientfun, args=(
        Target_IP, Target_PORT, TotalMessage / ProcessNumber , i, LogLevel , NumberPerSecond / ProcessNumber,protocol))
    ProccessArray[i].start()

for i in range(len(ProccessArray)):
    ProccessArray[i].join()

time2m = time.time()

difftime=time2m-time1m
count=TotalMessage
if LogLevel== 'log' or LogLevel == 'debug':
    print ('%i connect took %0.3f ms\t\teach connection take  %0.3f ms or %0.3f micros\t\t%i pers second' % (
        count, difftime * 1000.0, difftime * 1000.0 / count, difftime * 1000 * 1000 / count,int(count/difftime)))
