#!/usr/bin/env python
"""test the networking"""
from thread import start_new_thread
from time import sleep
from log import init_logging

from network import TCPServer
from network import TCPClient

def server(instance):
    """manage the server"""
    while True:
        scon = instance.accept()
        scon.rpc_listen()

def main():
    """run the test"""
    init_logging()
    tcpserver = TCPServer()
    start_new_thread(server, (tcpserver,))
    sleep(1)
    test = TCPClient('127.0.0.1')
    ccon = test.connect()
    ccon.rpc_call("help")

if __name__ == "__main__":
    main()
