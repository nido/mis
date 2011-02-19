#!/usr/bin/env python
from os.path import isdir
from os import makedirs
from logging import getLogger
from logging import DEBUG
from logging import INFO
from logging import WARN
from logging import StreamHandler
from logging.handlers import RotatingFileHandler
from logging import debug
from logging import info
from logging import warn
from logging import error
from logging import critical
from logging import Formatter

"""log.py is responsible for setting up the mis logging abilities.

Logging will be done to a file, and to the command-line. Release
versions will log warn messages and up in the console, and the
file will log info and up.

A brief rundown of the log levels as intended for this project:

Critical: Something is horribly wrong, and I don't know how to
    proceed. In fact, the only logical cause of action is to give
    up and exit(1); so that's what i'm gonna do.
Error: Something is very wrong. In fact, so wrong, that I need to
    cancel the current operation. Whatever I was about to do
    failed, but the system is still up and running.
Warn: Something went wrong. I don't know how, but this doesn't add
    up. However, I can still get the correct results, so i will
    proceed. Someone should take a look at what happened though.
Info: Just informing what is going to hapen in user terms. A
    description of the action to let know what is actually happening
    within the system.
Debug: These messages are most useful to see why something didn't
    work as expected. They give detailed information about certain
    steps in the system and are generally more useful to developpers
    then end users.

Logging will be done using the python built-in logging
functionality. Apparently it's pretty handy with that. This also
means one should be able to logger.getLogger a mis.whatever log and
start using it. The root log thus obviously is 'mis'.
"""

logfile = '/home/nido/.mis/user.log'
debuglogfile = '/home/nido/.mis/debug.log'

def init_logging():
	if not isdir('/home/nido/.mis/'):
		makedirs('/home/nido/.mis/')

	fileformatter = Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

	#pre-create the log file in order to check its existence.
	open(logfile, 'a').close() 
	open(debuglogfile, 'a').close() 

	rootlog = getLogger('mis')
	rootlog.setLevel(DEBUG)

	handler = RotatingFileHandler(logfile, maxBytes=1000, backupCount = 5)
	handler.setLevel(INFO)
	rootlog.addHandler(handler)

	handler = RotatingFileHandler(debuglogfile, maxBytes=1000, backupCount = 5)
	handler.setLevel(DEBUG)
	handler.setFormatter(fileformatter)
	rootlog.addHandler(handler)

	stderr = StreamHandler()
	handler.setFormatter(fileformatter)
	stderr.setLevel(WARN)
	rootlog.addHandler(stderr)

	rootlog.info('logging initialised.');
