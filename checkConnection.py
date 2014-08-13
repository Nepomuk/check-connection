#! /usr/bin/env python
"""
Check for an available internet conneciton by trying to get a DNS request
and then connect to it.
"""

import socket
import time

REMOTE_SERVER = "www.google.de"


def is_connected():
    """Tries to get a DNS reqeust and returns the success as boolean."""
    try:
        """See if we can resolve the host name.
        Tells us if there is a DNS listening."""
        host = socket.gethostbyname(REMOTE_SERVER)

        """Connect to the host.
        Tells us if the host is actually reachable."""
        socket.create_connection((host, 80), 2)
        return True
    except IOError:
        return False
    return False


def check_connection():
    """Continuously check the status of the connection."""
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


if __name__ == "__main__":
    check_connection()
