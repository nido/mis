#!/usr/bin/env python
"""main is basically the executable you'd run"""

from sys import argv
from os.path import abspath
from logging import getLogger

from log import init_logging
from pathwalker import Pathwalker
from consoleinput import Consoleinput
from database import Database

# Initialise logging
LOG = getLogger('mis.main')


def usage():
    """echos how to use this executable"""
    print "Usage: " + argv[0] + " command option"
    print """
help
    display this text.
index [directory]
    indexes the directory, or ../test_files when no argument is
    given and adds it to the couchdb database
batch
    asks you for keys and forces you to input that data for all entries in the database
"""


def index():
    """Indexes a directory"""
    path = abspath("../test_files")
    if len(argv) > 2:
        path = abspath(argv[2])
    walker = Pathwalker()   
    walker.evaluate_path(path)

def batch_update():
    """does a batch update through the console"""
    database = Database()
    meatware = Consoleinput()
    meatware.get_fieldnames()
    for entry in database.iterate_all_files():
        if len(entry) == 128:
            userdict = meatware.input_data()
            database.add_userdata(entry, userdict)
        
    

def main():
    """starts the program"""
    init_logging()

    if len(argv) > 1:
        if argv[1] == 'help':
            usage()
        if argv[1] == 'index':
            index()
        if argv[1] == 'batch':
            batch_update()
    else:
        usage()

main()

# vim: set tabstop=4 expandtab: #
