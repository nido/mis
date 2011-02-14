#!/usr/bin/env python
"""This script checks the media directory and adds the new files to the mis."""
from platform import node
from os import walk
from os.path import abspath
from os.path import isdir
from os import makedirs
from re import compile
from sys import argv
from hashlib import sha512
from mysql import insert_into_database
from mysql import test_if_in_database

from logging import getLogger
from logging import DEBUG
from logging.handlers import RotatingFileHandler


logfile = '/home/nido/.mis/add_media.log'

if not isdir('/home/nido/.mis/'):
	makedirs('/home/nido/.mis/')

open(logfile, 'a').close() 

log = getLogger('log')
log.setLevel(DEBUG)
handler = RotatingFileHandler(logfile, maxBytes=100, backupCount = 5)
log.addHandler(handler)


def main():
	if not len(argv) > 1:
		print """
Please run this program with as argument the folder you wish to index.
optionally, give a server name, otherwise, the hostname will be used.
"""
	
	walker = pathwalker()	
	walker.evaluate_path(abspath(argv[1]), pathwalker.add_file);

def get_filter():
	extensions=['avi', 'mpg', 'mp4', 'mkv', 'ogv', 'flv', 'ogg','mov']
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
			log.debug("not inserting " + filename)

main()
