"""media.py - governs files, tracks and data about them.

the point is to recognise (video) files and extracts properties
from them, and add them to the database. Video files might have
more video streams, of different characteristics, however, we
assume there is a 'primary' video stream of which we will use the
data. The file may also be a video container containing only
audio. In that case, it is not a video file but an audio file.

"""
from logging import getLogger
from mysql import save_container
from ffprobe import Prober

LOG=getLogger('mis.media')

class Container:
    """A container is an abstraction of the file's container. It
can pull information from raw_containers from ffprobes and from
the database and can save information to MIS from raw_containers as
well."""
    
    def __init__(self, filename, force_probe=False):
        if force_probe == False:
            LOG.warn('database reading not yet supported')
        self.key = None
        self.streamcount = None
        self.container_type = None
        self.duration = None
        self.size = None
        self.bitrate = None
        self.ffprobe_init(filename)

    def database_init(self, filename):
        pass

    def ffprobe_init(self, filename):
        probe = Prober(filename)

        if probe.raw_container.has_key('nb_streams'):
            self.streamcount = int(probe.raw_container['nb_streams'])
        else:
            LOG.error("There's no stream count in the container")
            return
        if probe.raw_container.has_key('format_name'):
            self.container_type = probe.raw_container['format_name']
        else:
            LOG.error("There is no container type defined")
            return
        if probe.raw_container.has_key('duration'):
           self.duration = int(float(
                    probe.raw_container['duration']) * 1000)
        else:
            LOG.warn("no duration found in continer")
            self.duration = None
        if probe.raw_container.has_key('size'):
            self.size = int(
                    probe.raw_container['size'].split('.')[0])
        else:
            LOG.error("There is no size in the container")
            return
        if probe.raw_container.has_key('bit_rate'):
            self.bitrate = int(
                    probe.raw_container['bit_rate'].split('.')[0])
        else:
            LOG.error("there is no bitrate defined in container")
            return
        

        save_container(self.streamcount, self.container_type, 
                self.duration, self.size, self.bitrate)

        def get_streamcount():
            """ returns the number of streams in the container"""
            return self.streamcount

        def get_type():
            """ returns the type of container"""
            return self.container_type

        def get_duration():
            """ returns the duration in usec"""
            return self.duration

        print(self.streamcount, self.container_type, 
                self.duration, self.size, self.bitrate)
        

class Stream:
    pass
# vim: set tabstop=4 expandtab textwidth=66: #
