#!/usr/bin/env python
"""This script checks the media directory and adds the new files to the mis."""
from platform import node
from os import walk
from os.path import abspath
from re import compile
from sys import argv
from hashlib import sha512
from mysql import insert_into_database
from mysql import test_if_in_database

def main():
	if not len(argv) > 1:
		print """
Please run this program with as argument the folder you wish to index.
optionally, give a server name, otherwise, the hostname will be used.
"""
	
	walker = pathwalker()	
	walker.evaluate_path(abspath(argv[1]));

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
		

	def evaluate_path(this, path):
		filter = get_filter()
		walker = walk(path)
		for item in walker:
			for file in item[2]:
				if(filter(file)):
					this.evaluate_file(item[0] + '/' + file)
			
	def evaluate_file(this, filename):
		if not test_if_in_database(filename):
			print "inserting " + filename
			sha512sum = sha512(open(filename).read()).hexdigest()
			insert_into_database(sha512sum, filename, True, this.nodename);
		else:
			print "not inserting " + filename

main()
