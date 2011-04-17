#!/usr/bin/env python
"""main is basically the executable you'd run"""

from sys import argv
from os import fork
from os.path import abspath
from logging import getLogger

from log import init_logging
from pathwalker import Pathwalker
from network import TCPServer
from network import TCPClient
from time import sleep

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

    walker = Pathwalker()   
    walker.evaluate_path(abspath("test_files"), Pathwalker.add_file)

    pid = fork()
    if pid != 0:
        test = TCPServer()
        connection = test.accept()
        connection.rpc_listen()
                

        #result = str(connection._recv())
        #open('output','w').write(result)
        #LOG.info(result)
        #print (result)
    else:
        sleep(1)
        test = TCPClient('127.0.0.1')
        connection = test.connect()
        if connection:
            x = connection.rpc_call("get filedatatest_files/test.avi")
            open("output", "w").write(x)
        else:  
            print("cannot connect to the server.")
        
    exit(1)

    if not len(argv) > 1:
        LOG.critical('No path is given, cannot continue')
        usage()
        exit(1)
    

main()

# vim: set tabstop=4 expandtab: #
