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

configuration
=============
configuration is done in two places. By hand in /etc/mis.conf, and
semi-automagically in ~/.mis/config. configuration files are done
using the configparser from python. This means we have .ini like config
files. These have sections, signified by the [] (e.g. [section_name]); and
options ("key = value" pairs). 

current configurable options are:
[loglevels]
name_of_log = loglevel

name_of_log as defined by the log. This should follow the
configuration 'mis.filename'. e.g. 'mis.pathwalker'
valid loglevel options are from least to most severe: 'debug', 'info', 'warn',
'error', 'critical'. Setting the log level ensures only logs from that level and higher
are logged. By default, only INFO and higher is considered for logging (including the debug log)



general list of todo stuff

clean up file extensions business (a.k.a. grab superiour list).
collections (of one episode, series, series of series, universes)
media/file/filetype/media-specifics recogniser.
`watched' list
double file checker
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

file
 +--container
    +--properties
    |   title
    |   year
    |   container_type
    |   media_type
    |   duration
    |   comment
    +--video streams
    |   codec
    |   width
    |   height
    |   framerate
    |   bitrate
    +--audio streams
    |   codec
    |   channels
    |   samlerate
    |   bitrate
    +--txt streams
    |   format
    +--picture streams
    |   format
    |   colours (TODO: expand)
    +--aux streams (are these interesting enough?




container
    primary properties:
        streams within container
    secondary properties:
        no specifics

streams:
--------

Video
    primary properties:
        type
        length (seconds.mmm)
        framerate
        aspect ratio
        width
        height
        avg.bitrate
    secondary properties:
        language

Audio
    primary properties:
        type
        length
        frequency
        sample rate (e.g. 8, 16, 24bit)
        abg.bitrate
    secondary properties:
        language

        
subpicture:
    primary:
        type
        length
        size (bytes)
    secondary:
        language

subtext:
    primary:
        type
        length
        size (bytes)
        primary colour
        secondary colour
        tertiary colour
        quaternary colour
    secondary:
        language

# vim: set tabstop=4 expandtab: #
