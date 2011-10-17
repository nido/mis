"""This script checks the media directory and adds the new files to the mis."""
from platform import node
from os import walk
from os import sep
from re import compile as regex
from sys import argv
from logging import getLogger
from hashlib import sha512 # pylint: disable-msg=E0611

from database import Database


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
        for item in walk(path):
            for filename in item[2]:
                if(finder(filename)):
                    self.add_file(item[0] + sep + filename)
            
    def add_file(self, filename):
        """A function which adds a file to the database"""
        if not self.database.path_exists(self.nodename, filename):
            LOG.info("inserting " + filename)
            sha512sum = sha512(open(filename).read()).hexdigest()
            self.database.add_path(sha512sum, self.nodename, filename)

# vim: set tabstop=4 expandtab textwidth=66: #
