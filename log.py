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

logfile = '/home/nido/.mis/add_media.log'

if not isdir('/home/nido/.mis/'):
        makedirs('/home/nido/.mis/')

#pre-create the log file
open(logfile, 'a').close() 



filelog = getLogger('log')
filelog.setLevel(WARN + 1)
handler = RotatingFileHandler(logfile, maxBytes=100, backupCount = 5)
filelog.addHandler(handler)

stderr = StreamHandler()
stderr.setLevel(INFO + 1)
errlog=getLogger('log').addHandler(stderr)


debug('debug works')
info('info works')
warn('warn works')
error('error works')
critical('critical works')
