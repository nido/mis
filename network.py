""" The network protocol is designed to allow two way communication through
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

from random import randint
from socket import socket
from socket import AF_INET
from socket import SOCK_STREAM
from socket import SO_REUSEADDR
from socket import SOL_SOCKET

from config import get_config
from logging import getLogger

LOG = getLogger('mis.network')

def bint32(x):
    """Turns a number into a 32bit byte array"""
    z=bytearray()
    for y in [3,2,1,0]:
        z.append((x / (256**y)) % 256)
    return z

class connection:
    """Responsible for the connection. Actual network stuff rather
    then the improvised protocol."""
    def __init__(self):
        pass

    def send(self, data):
        pass

    def recv(self, data):
        pass
    
class transaction:
    """the business of sending a request and getting a
    reply"""
    def __init__(self, con, data = None):
        """Initialises"""
        self.connection = self.counter()
        self.data = data
        self.outgoing = outgoing
        self.transaction_number = randint(0, 2**32);
        _transaction_counter += 1

    def execute():
        """Executes the transaction"""
        if data:
            self._send_command(data)
            return self._recv_data()
        else:
            data = self._recv_command()
            # TODO: parse/execute command)
            self.send_data(data)

    def _send_command(self, command):
        x = _packet(self)
        x.send()

    def _recv_command(self, command):
        pass
    def _send_data(self, data):
        pass
    def _recv_data(self, data):
        pass

    class _packet:
        """A single unit of data, size described in-packet"""
        def __init__(self, transaction):
            "initialise"
            self.payload = None
            self.id = None
            self.transaction_size = None
            self.packet_size = None
            self.data = None
            
            if transaction.data:
                self.payload = bytearray(transaction.data)
                self.id = bint32(
                        transaction.transaction_number)
                self.transaction_size = bint32(len(self.payload))
                self.packet_size = bint32(transaction_size +
                        len(self.id) +
                        len(self.transaction_size) + 4)
                self.data = (self.id + self.packet_size +
                        self.transaction_size + self.payload)


        def send(self):
            pass

        def recv(self):
            pass

class Daemon:
    """The daemon listens on a specified port and forwards
    set-up to a handler. The daemon is also required to verify it's
    peers and to secure the connection."""
    
    def __init__(self):
        """initialises"""
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
    client and exchange information and data. This handles the
    server portion"""
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
        
# vim: set tabstop=4 shiftwidth=4 expandtab textwidth=66 foldmethod=indent: #
