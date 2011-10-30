"""This script checks the media directory and adds the new files to the mis."""
from platform import node
from os import walk
from os import sep
from re import compile as regex
from sys import argv
from logging import getLogger
from hashlib import sha512 # pylint: disable-msg=E0611

from config import get_config
from database import Database
from ffprobe import Prober


LOG = getLogger('mis.pathwalker')


def get_filter():
    """a filter which takes out only filenames which probably contain media"""
    extensions = ['avi', 'mpg', 'mpeg', 'mp4', 'mkv', 'ogv', \
            'flv', 'ogg','mov', 'mp3', 'ac3', 'rm', 'ram', \
            'wmv', '3gp', 'aac', 'asf', 'h263', 'webm', 'm4a', \
            '3g2', 'mj2']
    regexstring = '\.('
    for extension in extensions:
        regexstring = regexstring + extension + '|'
    regexstring = regexstring[:-1] + ')$'
    return regex(regexstring).search

class Pathwalker:
    """The pathwalker is responsible recursively walk a directory
and apply a function to them."""

    def __init__(self):
        self.nodename = node()
        self.database = Database()
        if len(argv) > 2:
            self.nodename = argv[2]
        

    def evaluate_path(self, path):
        """Do the actual pathwalking. The pathwalker does not
accept files which are not in the native character set. This is
because filenames are saved in and retrieved from the database in
utf8, and do not translate back correctly. The default charset for
a filesystem according to mis is utf8. The default can be changed
in the configuration."""
        finder = get_filter()
        encoding = get_config().get('charsets', 'filesystem')
        for item in walk(path):
            try: 
                pathname = item[0].decode(encoding)
            except UnicodeDecodeError as error:
                LOG.warn("Could not add path " + pathname +
                        " because it is not in the filesystem's" +
                        " native encoding: " + error)
                continue
            for filename in item[2]:
                if(finder(filename)):
                    try: 
                        filename = filename.decode(encoding)
                    except UnicodeDecodeError as error:
                        LOG.warn("Could not add file " + filename
                                + ". because it is not in the " +
                                "filesystem's encoding: " + error)
                        continue
                    full_path = pathname + sep + filename
                    self.add_file(full_path)
                    self.add_ffprobe_data(full_path)

    def add_file(self, filename):
        """A function which adds a file to the database"""
        if not self.database.path_exists(filename,self.nodename):
            LOG.info("inserting " + filename)
            shasum = sha512(open(filename).read()).hexdigest()
            self.database.add_path(shasum, self.nodename, filename)

    def add_ffprobe_data(self, filename):
        """Adds ffprobe data to the database"""
        ffprobe = Prober(filename)
        ffprobe_data = ffprobe.get_properties()
        shasum = self.database.path_exists(filename, self.nodename)
        self.database.add_data(shasum, 'ffprobe', ffprobe_data)
        
# vim: set tabstop=4 expandtab textwidth=66: #
