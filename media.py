"""media.py - governs files, tracks and data about them.

the point is to recognise (video) files and extracts properties
from them, and add them to the database. Video files might have
more video streams, of different characteristics, however, we
assume there is a 'primary' video stream of which we will use the
data. The file may also be a video container containing only
audio. In that case, it is not a video file but an audio file.

"""
from platform import node
from logging import getLogger
from mysql import save_container
from mysql import find_container
from ffprobe import Prober

LOG = getLogger('mis.media')

class Container:
    """A container is an abstraction of the file's container. It
can pull information from raw_containers from ffprobes and from
the database and can save information to MIS from raw_containers as
well."""
    
    def __init__(self, filename, force_probe=False):
        """initialises a container, firstly, through the database,
if unavailable, or otherwise if forced, ffprobe is used."""
        self.key = None
        self.streamcount = None
        self.container_type = None
        self.duration = None
        self.size = None
        self.bitrate = None
        if force_probe == False:
            done = self.database_init(node(), filename)
            if done == True:
                return
            # fall back to ffprobe
        self.key = self.ffprobe_init(filename)

    def database_init(self, nodename, filename):
        """initialise using the database"""
        result = find_container(nodename, filename)
        if result == None:
            return False
        self.key = result[0]
        self.streamcount = result[1]
        self.container_type = result[2]
        self.duration = result[3]
        self.size = result[4]
        self.bitrate = result[5]
        return True

    def ffprobe_init(self, filename):
        """initialise using ffprobe"""
        probe = Prober(filename)

        if not probe.raw_container.has_key('nb_streams'):
            LOG.error("There's no stream count in the container")
            return
        self.streamcount = int(probe.raw_container['nb_streams'])

        if not probe.raw_container.has_key('format_name'):
            LOG.error("There is no container type defined")
            return
        self.container_type = probe.raw_container['format_name']

        if probe.raw_container.has_key('duration'):
            self.duration = int(float(
                    probe.raw_container['duration']) * 1000)
        else:
            LOG.warn("no duration found in continer")
            self.duration = None
        if not probe.raw_container.has_key('size'):
            LOG.error("There is no size in the container")
            return
        self.size = int(
                probe.raw_container['size'].split('.')[0])
        if not probe.raw_container.has_key('bit_rate'):
            LOG.error("there is no bitrate defined in container")
            return
        self.bitrate = int(
                probe.raw_container['bit_rate'].split('.')[0])
        
        container = save_container(self.streamcount, self.container_type, 
                self.duration, self.size, self.bitrate)
        return container
        
# vim: set tabstop=4 expandtab textwidth=66: #
