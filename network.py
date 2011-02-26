"""network.py is responsible for the primary network functions.
This includes keeping a socket open."""

from socket import socket
from socket import AF_INET
from socket import SOCK_STREAM
from socket import SO_REUSEADDR
from socket import SOL_SOCKET

from config import get_config
from logging import getLogger

LOG = getLogger('mis.network')

class Daemon:
    """The daemon listens on a specified port and forwards
set-up to a handler. The daemon is also required to verify it's
peers and to secure the connection."""

    def __init__(self):
        config = get_config()
        host = config.get('network', 'host')
        port = int(config.get('network', 'port'))
        s = socket(AF_INET, SOCK_STREAM )
        s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        LOG.debug('started socket on "' + str(host) + '" port "' +
                str(port) + '". binding')
        s.bind((host, port))
        LOG.debug('bind complete, listen(1)ing')
        s.listen(0)
        LOG.debug('accepting')
        conn, addr = s.accept()
        LOG.info('Got a connection from ' + str(addr))
        bla = server_handler(conn,addr)


class server_handler:
    """The handler is given a socket to which to talk to another
client and exchange information and data."""
    def __init__(self, conn, addr):
        """initiates a server process"""
        self.connection = conn
        self.address = addr
        # let's keep it simple for now and just grab and print
        # everything
        while True:
            # "we're logging; 80 chars a time"
            bla = conn.recv(80)
            getLogger('mis.network.server_handler.traffic').debug(bla)
            
        print bla
        print "done"

# vim: set tabstop=4 expandtab textwidth=66: #
