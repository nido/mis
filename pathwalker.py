"""This script checks the media directory and adds the new files to the mis."""
from platform import node
from os import walk
from re import compile as regex
from sys import argv
from hashlib import sha512 # pylint: disable-msg=E0611
from mysql import save_file
from mysql import test_if_in_database
from media import Container

from logging import getLogger

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
        if len(argv) > 2:
            self.nodename = argv[2]
        

    def evaluate_path(self, path, method):
        """Do the actual pathwalking"""
        finder = get_filter()
        walker = walk(path)
        for item in walker:
            for filename in item[2]:
                if(finder(filename)):
                    method(self, item[0] + '/' + filename)
            
    def add_file(self, filename):
        """A function which adds a file to the database"""
        if not test_if_in_database(filename):
            LOG.info("inserting " + filename)
            container = Container(filename, force_probe = True)
            sha512sum = sha512(open(filename).read()).hexdigest()
            save_file(sha512sum, filename, active=True,
                    nodename=self.nodename, container_id = 
                    container.key)
        else:
            LOG.debug("already know" + filename + ", ignoring")

# vim: set tabstop=4 expandtab: #
