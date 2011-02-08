#!/usr/bin/env python
"""This script checks the media directory and adds the new files to the mis."""
from os import walk
from os.path import abspath
from re import compile
from sys import argv
from hashlib import sha512
from mysql import insert_into_database
from mysql import test_if_in_database

def main():
	evaluate_path(abspath(argv[1]));

def get_filter():
	extensions=['avi', 'mpg', 'mp4', 'mkv', 'ogv', 'flv', 'ogg','mov']
	regexstring = '\.(';
	for extension in extensions:
		regexstring = regexstring + extension + '|'
	regexstring = regexstring[:-1] + ')$'
	return compile(regexstring).search

def evaluate_path(path):
	filter = get_filter()
	walker = walk(path)
	for item in walker:
		for file in item[2]:
			if(filter(file)):
				evaluate_file(item[0] + '/' + file)
#find /var/data/media/video -type f | while read line; do evaluate_file "$line"; done
			
def evaluate_file(filename):
	if not test_if_in_database(filename):
		print "inserting " + filename
		sha512sum = sha512(open(filename).read()).hexdigest()
		insert_into_database(sha512sum, filename, True);
	else:
		print "not inserting " + filename
#        FILE=`echo "$1" | sed "s/'/\\\\'/g" | sed 's/"/\\"/g' | sed 's|\|\\\\|'`
#echo file "$FILE"
#        echo "select 1 from files where path like '$FILE'" | mysql mis
#        TEST=`echo "select 1 from files where path like '$FILE'" | mysql mis`
#test -n "$TEST" && echo test "$TEST"
#        test -z "$TEST" && insert_into_database "$1"

main()
