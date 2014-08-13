#! /usr/bin/env python

import socket
import time

REMOTE_SERVER = "www.google.de"
def is_connected():
    try:
        # see if we can resolve the host name -- tells us if there is
        # a DNS listening
        host = socket.gethostbyname(REMOTE_SERVER)
        # connect to the host -- tells us if the host is actually
        # reachable
        s = socket.create_connection((host, 80), 2)
        return True
    except:
        pass
        return False


connectionLost = -1
while True:
    # print "Testing at {0}".format(time.strftime("%c"))
    if not is_connected():
        if connectionLost < 0:
            connectionLost = time.time()
    else:
        if connectionLost > 0:
            if time.time() - connectionLost > 1:
                print("Connection lost at {0} and back online at {1}  (Offline for {2:.0f} s)".format(time.strftime("%c", time.localtime(connectionLost)), time.strftime("%c"), (time.time() - connectionLost)))
            connectionLost = -1
        time.sleep(1)
