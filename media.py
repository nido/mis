"""media.py - governs files, tracks and data about them.

the point is to recognise (video) files and extracts properties
from them, and add them to the database. Video files might have
more video streams, of different characteristics, however, we
assume there is a 'primary' video stream of which we will use the
data. The file may also be a video container containing only
audio. In that case, it is not a video file but an audio file.

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

"""

# vim: set tabstop=4 expandtab: #
