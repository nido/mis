#!/usr/bin/env python
from thread import start_new_thread
from time import sleep
from log import init_logging

from network import TCPServer
from network import TCPClient

init_logging()

def server(test):

	
	while True:
		con = test.accept()
		con.rpc_listen()
test = TCPServer()
start_new_thread(server, (test,))
sleep(1)
test = TCPClient('127.0.0.1')
con = test.connect()
con.rpc_call("help")

