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

def intb4(x):
    """Turns a number into a 32bit byte array"""
    z=bytearray()
    for y in [3,2,1,0]:
        z.append((x / (256**y)) % 256)
    return z

def b4int(x):
    """Turns a 32bit byte array into a number"""
    z=0
    for y in (0,1,2,3):
        z = z + x[3-y]*(256**y)
    return z


class Connection:
    """Responsible for the connection. Actual network stuff rather
    then the improvised protocol."""
    def __init__(self, socket, conn=None, addr=None):
        self.socket = socket
        self.connection = conn
        self.remote_address = addr

    def send(self, data):
        """Takes a bytestring and sends it off to the other side.
        The Connection is responsible for handeling protocols used
        by this program, and strips off this excess information"""
        # we send and receive packets.
        packet = bytearray()
        # Let's just add a size argument for now
        packet += intb4(len(data)+4)
        packet += bytearray(data)
        return self.socket.send(packet)

    def recv(self):
        """receives a packet from the network and returns its
        bytestream"""
        print self.socket
        packet = self.socket.recv(4)
        print packet
        packet = bytearray(packet)
        packet_size = b4int(packet)
        packet = packet + bytearray(self.socket.recv(packet_size))
        return packet[4:]
    
    
class TCPServer:
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
        LOG.debug('bind complete')

    def accept(self):
        """Returns a connection made by listening to the port."""
        self.socket.listen(1)
        LOG.debug('accepting')
        conn, addr = self.socket.accept()
        LOG.info('Got a connection from ' + str(addr))
        return Connection(self.socket, conn, addr)

class TCPClient:
    """The tcp client creates a tcp connection to the server."""
    
    def __init__(self, host, port=None):
        config = get_config()
        self.port = int(config.get('network', 'port'))
        self.host = host
        if port:
            self.port = port
        self.socket = socket(AF_INET, SOCK_STREAM)
        self.socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

    def connect(self):
        """activates the connection and returns the Connection"""
        self.socket.connect((self.host, self.port))
        return Connection(self.socket, None, self.host)


# vim: set tabstop=4 shiftwidth=4 expandtab textwidth=66 foldmethod=indent: #
