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
        bla = handler(conn,addr)


class handler:
    """The handler is given a socket to which to talk to another
client and exchange information and data."""
    def __init__(self, conn, addr):
        print conn, addr
        bla = conn.recv(1024)
        print bla
        print "done"

# vim: set tabstop=4 expandtab textwidth=66: #
