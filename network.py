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

class network:
    """
The network protocol is designed to allow two way communication through
a single tcp connection. After a connection is made, both nodes may assume
the client role of a normal client-server model.

the size of requests/replies can vary from a boolean value to 'the
complete media library'. E.g. In case node A makes a big request to
node B, at the very least node B should be able to take requests from node A.

Because of this, we use a little 'network' protocol within the network protocol.
The purpose of this protocol is to 'emulate' a bidirectional rcp connections
over a single tcp connection.


the client of the tcp connection is called node A. the server of
the tcp connection is node B. Each transmission is tagged with 
the originating rpc node, a transaction identifier, and a package size field,
and a request/response size field.

To start of with the transaction identifier, since nodes should be
able to send multiple requests to the other server, it makes sense
to identify them individually over the single connection.

the originating rpc node identifier allows for both hosts to have a 
individual pool of transaction numbers, eliminating the need to synchronise
transaction numbers.

the message size field is the size of the complete message,
excluding overhead from the package(s) used, this allows to track wether
or not a request is fulfilled without knowing about the underlying data.

the package size is the size of the current packet, including the overhead
of the headers. this allows to identify packages regarding the underlying
structure or protocol.


we rely on underlying protocols to guarantee us a complete, sequential
and correct bitstream. Therefore we do not use error correction/checking,
sequence numbers or other safeguards. However, the protocol should be
implemented to allow later versions of the protocol and negotiation
on which version to use, in order to allow extensions in the future
SSL encryption should be
used as well in order to further guarantee integrity of the bitsream.
    """

    class _transaction:
        """the business of sending a request and getting a
reply"""
#message
        pass

    class _message:
        """one part of the transmission, a message goes one way"""
# body

    class _packet:
        """A single unit of data, size described in-packet"""
        def __init__():
            "initialise"
            this.size = None

    class _connection:
        """something to represent the tcp connection"""
        pass

    def rpc_call(data):
        """make a call, get a reply. may take a while though"""
        pass

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
