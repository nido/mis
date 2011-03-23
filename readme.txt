Media Information System
========================

Needed packages:
- Python
- Python-MySQL (fedora: MySQL-python)

This is an attempt to make it feasable to handle media libraries
of ridiculous proportions. Because of that, it uses a library of
its own asynchronously from the accurate metadata in the file.

Rediculous proportions at time of writing means bigger then two
terabyte. more generally speaking: more then fits on a single unit
of (consumer) storage, more then can be read completely (by the computer) in
24 hours, and more entries then can be cached by the processor.

This means it should synchronise from time to time and the media
library itself should be reasonably static. Should the data get too much
out of sync, mis becomes worthless; so be sure to activate the
synchronisation when any is created.

the files are also decoupled from the actual media. This is handy
should one have three copies of a single media. support for
divided (e.g. film_part1.mpg and film_part2.mpg) may be included
in the future.

there is an 'active' boolean in the files list. this should be
deactivated rather then the entry removed once the file is
unavailable or replaced with another copy (given the sha1 hash).
development is underway to allow redundancy of files or media
over different sites.

network protocol
================
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

the request/response size field is the size of the complete request/reply,
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

configuration
=============
configuration is saved in three places. The (complete) default configuration
is set up and saved in-code. /etc/mis.conf is read as system wide setting, and
~/.mis/config is read as user settings. Keep in mind, system  config always takes
precedence over default config and user config always takes precedense over system
config. All entries are included to the config, even if they seem nonsensical.

Configuration files are done
using the configparser from python. This means we have .ini like config
files. These have sections, signified by the [] (e.g. [section_name]); and
options ("key = value" pairs). 

current configurable options are described in the default config at config.py

name_of_log as defined by the log. This should follow the
configuration 'mis.filename'. e.g. 'mis.pathwalker'
valid loglevel options are from least to most severe: 'debug', 'info', 'warn',
'error', 'critical'. Setting the log level ensures only logs from that level and higher
are logged. By default, only INFO and higher is considered for logging (including the debug log)

SHA512 hash
===========
Within this application, at least in the beinning, the sha512 hash will
be assumed to be a perfect hashing algorithm. However, in reality, it is
not.

According to the principles of the birthday attack; at 1.25 * sqrt(2**512) =
1.4474011154664524e+77 we can expect to have a collision. 

in fact, here's a nice list courticy of wikipedia
Desired probability of random collision (p)
10e−18  10e−15  10e−12  10e−9   10e−6   0.1%    1%      25%     50%     75%
1.6e68  5.2e69  1.6e71  5.2e72  1.6e74  5.2e75  1.6e76  8.8e76  1.4e77  1.9e77

so you can be about 99.9999999999999999% sure you have no collisions and have
160000000000000000000000000000000000000000000000000000000000000000000 files indexed.

general list of todo stuff
==========================

integration:
    unittests

cleanup:
    media-specifics recogniser.
    clean up file extensions business (a.k.a. grab superiour list).

extensions:
    collections (of one episode, series, series of series, universes)
    `watched' list
    double signature checker
    connect to external instance
        up/download files
    talk to the admin (missing/double files, other problems)
    redundant jbod storage usage/detection
        storage importance settings (unimportant - no redundancy,
        	superimportant - omnipresent redundancy)

user interface


containers:
-----------

containers are the part of the file which holds it all together.
they coordinate the interleave between video and audio frames,
contain general information and usually also information about the
streams within them. containers contain multiple streams. They
usually contain a title but are not uniquely identifiable by it.

Okay. Back to reality. The container kinda meta-is the media. it
contains info we want

# vim: set tabstop=4 expandtab: #
