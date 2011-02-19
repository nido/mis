#!/usr/bin/env python

from sys import argv
from os.path import abspath
from log import init_logging
from logging import getLogger
init_logging()
from pathwalker import pathwalker

log = getLogger('mis.main')
def usage():
    print """
Please run this program with as argument the folder you wish to index.
optionally, give a server name, otherwise, the hostname will be used.
"""

def main():
    if not len(argv) > 1:
        log.critical('No path is given, cannot continue')
        usage()
        exit(1)
    
    walker = pathwalker()   
    walker.evaluate_path(abspath(argv[1]), pathwalker.add_file);

main()

# vim: set tabstop=4 expandtab: #
