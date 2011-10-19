"""ffprobe.py is a python module that wraps around ffprobe

The function is to extract stream and container information. The
module wraps around ffprobe which will imply some compatibility
issues for windows computers. One needs to install ffmpeg to get
this program to work propertly. The program should still function,
albeit degraded, without ffprobe. In this case, all media will
have empty containers without streams."""

from chardet import detect

from config import get_config
from logging import getLogger
from subprocess import Popen
from subprocess import PIPE

LOG = getLogger('mis.ffprobe')

def test_ffprobe():
    """tests whether ffprobe works by running 'ffprobe
-version'"""
    result = False
    command = ['ffprobe', '-version']
    ffprobe = Popen(command, stdout = PIPE, stderr = PIPE)
    return_code = ffprobe.wait()
    if return_code == 0:
        result = True
    return result

def _correct_encoding(string):
    """values in files can have character encodings different from
unicode. This function tries to correctly decode them by letting
chardet guess the character set used. If the detected character
set cannot decode the string, latin1 is used as fallback."""
    charset = detect(string)['encoding']
    goodstring = None
    try:
        goodstring = string.decode(charset)
    except (UnicodeDecodeError, TypeError) as error:
        LOG.info('Character encoding detection failed: ' +
                str(error))
        charset = get_config().get('charsets', 'fallback')
    if goodstring == None:
        LOG.info('using fallback (' + charset + ')')
        try:
            goodstring = string.decode(charset)
        except (UnicodeDecodeError, TypeError) as error:
            LOG.warn("Couldn't decode string as fallback encoding.")
    
    if goodstring == None:
        goodstring = string.decode('latin1')
    return goodstring


class Prober:
    """The superclass prober, the one that does the probing."""

    def __init__(self, filename):
        """initialises the prober"""
        LOG.debug('probe for ' + filename + ' initialised')
        # open files in the filesystem's default encoding
        encoding = get_config().get('charsets', 'filesystem')
        self.filename = filename
        self.raw_filename = filename.encode(encoding)
        self.raw_container = None
        self.raw_streams = None
        self.raw_tags = None
        self.raw_output = None
        self.data = None


    def process_file(self):
        """execute the program and read the file"""
        command = ["ffprobe", "-loglevel", "quiet",
                "-show_format", "-show_streams", self.raw_filename]
        ffprobe = Popen(command, stdout = PIPE, stderr = PIPE)
        return_code = ffprobe.wait()
        if return_code != 0:
            LOG.error('ffprobe command failed: ' +
                    reduce(lambda s,y: s + ' ' + y,command))
            return None
        return ffprobe.stdout.read()

    def extract_tags(self):
        """Takes the TAG:key values from the streams and containers
and puts them into their own tag dictionary (minus the TAG:
part)"""
        tag_sources = self.raw_streams + [self.raw_container]
        for dictionary in tag_sources:
            for key in dictionary.keys():
                if key[:4] == 'TAG:':
                    self.raw_tags = {}
                    value = dictionary.pop(key)
                    self.raw_tags[key[4:]] = value

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
        if self.raw_output == None:
            self.raw_output = self.process_file()
        self.raw_streams = []
        self.raw_container = {}
        current_node = None
        current_key = None # track the key (to survive newlines)
        lines = ''
        if self.raw_output != None:
            lines = self.raw_output.split('\n')

        for line in lines:
            if(line == '[STREAM]'): #start of a new stream
                new_dict = {}
                self.raw_streams.append(new_dict)
                current_node = new_dict
            elif(line == '[FORMAT]'): # start of a new container
                current_node = self.raw_container
            elif(line[:2] == '[/'): # end of a stream/container
                current_node = None
            elif current_node != None: # data line
                temp = line.split('=', 1)
                if (len(temp) > 1) and (temp[1] != ''):
                    current_node[temp[0]] = _correct_encoding(temp[1])
                    current_key = temp[0]
                else:
                    current_node[current_key] += "\n" + _correct_encoding(line)
            else:
                if line != '': # empty lines are expected.
                    LOG.warn('found "' + line + '" outside of ' +
                            ' a STREAM/FORMAT block')
        self.extract_tags()

    def get_properties(self):
        """Returns the results of the ffprobe"""
        if self.data == None:
            if(self.raw_container == None or self.raw_streams == None):
                self.parse()
        self.data = {'container': self.raw_container, 
                'streams': self.raw_streams}
        if self.raw_tags:
            self.data['tags'] = self.raw_tags
        return self.data

# vim: set tabstop=4 expandtab textwidth=66: #
