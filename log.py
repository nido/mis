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
from os.path import isdir
from os import makedirs
from logging import getLogger
from logging import DEBUG
from logging import INFO
from logging import WARN
from logging import ERROR
from logging import CRITICAL
from logging import StreamHandler
from logging.handlers import RotatingFileHandler
from logging import Formatter
from config import get_config

LOGFILE = '/home/nido/.mis/user.log'
DEBUGLOGFILE = '/home/nido/.mis/debug.log'

LOG = getLogger('mis.log')

STR_LVL = {"debug": DEBUG,
        "info": INFO,
        "warn": WARN,
        "error": ERROR,
        "critical": CRITICAL}

LVL_STR = dict((v, k) for k, v in STR_LVL.iteritems())


def get_loglevel(string):
    """returns the loglevel belonging to a string"""
    result = None
    if STR_LVL.has_key(string):
        result = STR_LVL[string]
    else:
        LOG.warn("loglevel '" + string + "' is unknown")
    return result

def set_loglevels():
    """Sets the loglevels as configured (be config file later)"""
    section = 'loglevels'
    getLogger('mis.config').setLevel(DEBUG)
    cfg = get_config()
    level_config = cfg.list_section(section)
    if level_config != None:
        for setting in level_config:
            value = cfg.get(section, setting)
            loglevel = get_loglevel(value)
            if loglevel == None:
                LOG.error("The config states an illegal loglevel for "
                        + section)
            else:
                LOG.info("setting custom loglevel " +
                        LVL_STR[loglevel] + " for " + setting)
                getLogger(setting).setLevel(loglevel)

def init_logging():
    """initialises logging"""
    if not isdir('/home/nido/.mis/'):
        makedirs('/home/nido/.mis/')

    fileformatter = Formatter("%(asctime)s - %(name)s - " + \
            "%(levelname)s - %(message)s")

    #pre-create the log file in order to check its existence.
    open(LOGFILE, 'a').close() 
    open(DEBUGLOGFILE, 'a').close() 

    rootlog = getLogger('mis')
    rootlog.setLevel(INFO)

    handler = RotatingFileHandler(LOGFILE, maxBytes=10000000, backupCount = 5)
    handler.setLevel(INFO)
    handler.setFormatter(fileformatter)
    rootlog.addHandler(handler)

    handler = RotatingFileHandler(DEBUGLOGFILE, maxBytes=10000000,
            backupCount = 5)
    handler.setLevel(DEBUG)
    handler.setFormatter(fileformatter)
    rootlog.addHandler(handler)

    stderr = StreamHandler()
    handler.setFormatter(fileformatter)
    stderr.setLevel(WARN)
    rootlog.addHandler(stderr)

    set_loglevels()

    LOG.info('logging initialised.')
# vim: set tabstop=4 expandtab: #
