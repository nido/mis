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
from ffprobe import test_ffprobe
from ffprobe import Prober


LOG = getLogger('mis.pathwalker')


def get_filter():
    """a filter which takes out only filenames which probably contain media"""
    extensions = ['avi', 'mpg', 'mpeg', 'mp4', 'mkv', 'ogv', \
            'flv', 'ogg','mov', 'mp3', 'ac3']
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
        """Do the actual pathwalking"""
        finder = get_filter()
        encoding = get_config().get('charsets', 'filesystem')
        for item in walk(path):
            try: 
                pathname = item[0].decode(encoding)
            except UnicodeDecodeError as e:
                LOG.warn("Could not add path " +
                        filename + ". because it is not in the filesystem's encoding." + e)
            else:
                for filename in item[2]:
                    if(finder(filename)):
                        try: 
                            filename = filename.decode(encoding)
                        except UnicodeDecodeError as e:
                            LOG.warn("Could not add file " +
                                    filename + ". because it is not in the filesystem's encoding." + e)
                        else:
                            full_path = pathname + sep + filename
                            self.add_file(full_path)
            
    def add_file(self, filename):
        """A function which adds a file to the database"""
        if not self.database.path_exists(self.nodename, filename):
            LOG.info("inserting " + filename)
            sha512sum = sha512(open(filename).read()).hexdigest()
            self.database.add_path(sha512sum, self.nodename, filename)
            self.add_ffprobe_data(sha512sum, filename)

    def add_ffprobe_data(self, shasum, filename):
        """Adds ffprobe data to the database"""
        LOG.info("adding ffprobe data for " + filename)
        ffprobe = Prober(filename)
        ffprobe_data = ffprobe.get_properties()
        self.database.add_data(shasum, 'ffprobe', ffprobe_data)
        
# vim: set tabstop=4 expandtab textwidth=66: #
