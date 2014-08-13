#! /usr/bin/env python
"""
Check for an available internet conneciton by trying to get a DNS response
and then connect to it.
"""

import sys
import socket
import time
import argparse

# Default values
REMOTE_SERVER = "www.google.de"
OFFLINE_MIN = 1   # (in seconds) disregard short connection losses


def is_connected(server):
    """Tries to get a DNS reqeust and returns the success as boolean."""
    try:
        """See if we can resolve the host name.
        Tells us if there is a DNS listening."""
        host = socket.gethostbyname(server)

        """Connect to the host.
        Tells us if the host is actually reachable."""
        socket.create_connection((host, 80), 2)
        return True
    except IOError:
        pass
    return False


def check_connection(args):
    """Continuously check the status of the connection."""
    connectionLostAt = -1
    while True:
        # print "Testing at {0}".format(time.strftime("%c"))
        if not is_connected(args.remote_server):
            if connectionLostAt < 0:
                connectionLostAt = time.time()
                print "Connection lost at {0}".format(time.strftime("%c")),
                sys.stdout.flush()
        else:
            if connectionLostAt > 0:
                # print out something if disconnect is longer than offline_min
                if time.time() - connectionLostAt > args.offline_min:
                    print "and back online at {0}  (Offline for {1:.0f} s)".format(
                        time.strftime("%X"),
                        (time.time() - connectionLostAt)
                    )
                # otherwise reset current output line
                else:
                    print "\r"+50*" "+"\r",
                    sys.stdout.flush()
                connectionLostAt = -1

        # wait a bit
        time.sleep(0.5)


def main():
    """The main function that is called automatically."""
    parser = argparse.ArgumentParser(
        description='Check for an available internet connection by trying \
            to get a DNS response and then connect to it.')
    parser.add_argument(
        '-o', '--offline-min',
        type=int, default=OFFLINE_MIN,
        help="disconnects shorter than this (in seconds) are disregarded")
    parser.add_argument(
        '--remote-server',
        type=str, default=REMOTE_SERVER,
        help="the remote server to connect to")
    args = parser.parse_args()

    # now check the connection
    check_connection(args)



if __name__ == "__main__":
    main()
