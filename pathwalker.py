#!/usr/bin/env python
"""This script checks the media directory and adds the new files to the mis."""
from platform import node
from os import walk
from re import compile
from sys import argv
from hashlib import sha512
from mysql import insert_into_database
from mysql import test_if_in_database

from logging import getLogger

log = getLogger('mis.pathwalker')


def get_filter():
    extensions=['avi', 'mpg', 'mpeg', 'mp4', 'mkv', 'ogv', 'flv', 'ogg','mov', 'mp3', 'ac3']
    regexstring = '\.(';
    for extension in extensions:
        regexstring = regexstring + extension + '|'
    regexstring = regexstring[:-1] + ')$'
    return compile(regexstring).search

class pathwalker:

    def __init__(this):
        this.nodename = node()
        if len(argv) > 2:
            this.nodename = argv[2]
        

    def evaluate_path(this, path, method):
        filter = get_filter()
        walker = walk(path)
        for item in walker:
            for file in item[2]:
                if(filter(file)):
                    method(this, item[0] + '/' + file)
            
    def add_file(this, filename):
        if not test_if_in_database(filename):
            log.info("inserting " + filename)
            sha512sum = sha512(open(filename).read()).hexdigest()
            insert_into_database(sha512sum, filename, True, this.nodename);
        else:
            log.debug("already know" + filename + ", ignoring")

# vim: set tabstop=4 expandtab: #
