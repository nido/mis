#!/usr/bin/env python
"""main is basically the executable you'd run"""


from sys import argv
from os.path import abspath
from log import init_logging
from logging import getLogger
from pathwalker import Pathwalker

LOG = getLogger('mis.main')
def usage():
    """echos how to use this executable"""
    print """
Please run this program with as argument the folder you wish to index.
optionally, give a server name, otherwise, the hostname will be used.
"""

def main():
    """starts the program"""
    init_logging()
    if not len(argv) > 1:
        LOG.critical('No path is given, cannot continue')
        usage()
        exit(1)
    
    walker = Pathwalker()   
    walker.evaluate_path(abspath(argv[1]), Pathwalker.add_file)

main()

# vim: set tabstop=4 expandtab: #
