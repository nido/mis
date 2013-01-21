#!/usr/bin/env python
"""main is basically the executable you'd run"""

from sys import argv
from os.path import abspath
from logging import getLogger

from log import init_logging
from consoleinput import Consoleinput
from consoleinput import Console
from database import Database
from commands import index
from commands import usage
from consoleinput import batch_update

# Initialise logging
LOG = getLogger('mis.main')

def main():
    """starts the program"""
    init_logging()

    if len(argv) > 1:
        print "Usage: " + argv[0] + " [command [option]]"
        if argv[1] == 'help':
            usage()
        if argv[1] == 'index':
            path = '../test_files'
            if len(argv) > 2:
                path = abspath(argv[2])
            index(path)
        if argv[1] == 'batch':
            batch_update()
    else:
        console = Console()
        usage()
        console.attach()

main()

# vim: set tabstop=4 expandtab: #
