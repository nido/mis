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
        self.host = config.get('network', 'host')
        self.port = int(config.get('network', 'port'))
        self.socket = socket(AF_INET, SOCK_STREAM)
        self.socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        LOG.debug('started socket on "' + str(self.host) + '" port "' +
                str(self.port) + '". binding')
        self.socket.bind((self.host, self.port))
        LOG.debug('bind complete, listen(1)ing')
        self.socket.listen(1)
        LOG.debug('accepting')
        conn, addr = self.socket.accept()
        LOG.info('Got a connection from ' + str(addr))
        ServerHandler(conn, addr)


class ServerHandler:
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
            getLogger('mis.network.Server_handler.traffic').debug(bla)
            
        print bla
        print "done"

# vim: set tabstop=4 expandtab textwidth=66: #
