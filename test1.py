import sys, getopt
if __name__ == '__main__':

    controllers=None
    UDP_PORT=None
    argv = sys.argv[1:]

    opts, args = getopt.getopt(argv, "hi:p:l:", ["ip=", "port=", "loglevel="])

    print str(opts)
    print str(args)
    """
    for opt, arg in opts:
        if opt == '-h':
            print 'clientside.py -i <ip> -o <port>'
            sys.exit()
        elif opt in ("-i", "--ip"):
            controllers = arg
        elif opt in ("-p", "--port"):
            Target_PORT = int(arg)

    for controllerIP in controllers:
        print controllerIP
    print Target_PORT
    """