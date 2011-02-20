"""ffprobe.py is a python module that wraps around ffprobe

The function is to extract stream and container information. The
module wraps around ffprobe which will imply some compatibility
issues for windows computers. One needs to install ffmpeg to get
this program to work propertly. The program should still function,
albeit degraded, without ffprobe. In this case, all media will
have empty containers without streams."""

from logging import getLogger
from subprocess import Popen
from subprocess import PIPE

LOG = getLogger('mis.ffprobe')

class Prober:
    """The superclass prober, the one that does the probing."""

    def __init__(self, filename):
        """initialises the prober"""
        LOG.debug('probe for ' + filename + ' initialised')
        self.filename = filename
        self.raw_container = None
        self.raw_streams = None
        self.parse()
        print self.raw_container
        print self.raw_streams


    def process_file(self):
        """execute the program and read the file"""
        command = ["ffprobe", "-loglevel", "quiet",
                "-show_format", "-show_streams", self.filename]
        ffprobe = Popen(command, stdout = PIPE, stderr = PIPE)
        return_code = ffprobe.wait()
        if return_code != 0:
            LOG.error('ffprobe command failed: ' +
                    reduce(lambda s,y: s + ' ' + y,command))
            return None
        return ffprobe.stdout.read()

    def parse(self):
        """does actual parsing. Happily enough, ffprobe returns
inifile-like output. streams are preceded by [STREAM], containers
are preceded by [FORMAT], and these blocks are closed in html-like
fashion [/whatever]. Within these, there's just name = value
pairs.

The blocks are recognised and self.raw_streams is extended and the new
entry is set as the current_node. if it is a [FORMAT] block the
container is set as the current node. in case of a closing block,
current node is closed. The key=value pairs are added to the
current node dictionary"""
        LOG.debug('parsing ' + self.filename)
        raw_output = self.process_file()
        self.raw_streams = []
        self.raw_container = {}
        current_node = None
        for line in raw_output.split('\n'):
            if(line == '[STREAM]'):
                new_dict = {}
                self.raw_streams.append(new_dict)
                current_node = new_dict
            elif(line == '[FORMAT]'):
                current_node = self.raw_container
            elif(line[:2] == '[/'):
                current_node = None
            elif current_node != None:
                temp = line.split('=')
                current_node[temp[0]] = temp[1]
            else:
                if line != '':
                    LOG.warn('found "' + line + '" outside of ' +
                            ' a STREAM/FORMAT block')

    def get_container(self):
        """returns the container related to this prober"""
        LOG.debug('getting container for ' + self.filename)

    def get_stream(self, streamno):
        """returns stream streamno from this prober"""
        LOG.debug('getting stream ' + streamno + ' for ' +
                self.filename)


# vim: set tabstop=4 expandtab textwidth=66: #
