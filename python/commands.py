""" command is the part of the program which parses commands given
    to the system and checks authorisation for said commands, and
    initiates the appropriate backend command (probably network,
    database or maybe probe)"""
from logging import getLogger
from os.path import abspath
from os.path import exists

from database import Database

LOG = getLogger('mis.commands')

def get_function(string):
    """ Returns a tuple containing the string and accompanying
        argument. Returns None on an invalid command"""
    command = None
    argument = None
    result = None
    for name in COMMAND_DICT:
        if name == string[:len(name)]:
            command = COMMAND_DICT[name]
            argument = string[len(name):]
            break # optimisation: breakout of for loop
    if command == None:
        LOG.info('received invalid command:')
        LOG.info(string)
    else:
        result = (command, argument)
    return result

def get_command(function):
    """ Returns the command string that belongs to the function,
        or None."""
    result = None
    for name in COMMAND_DICT:
        if COMMAND_DICT[name] == function:
            result = name
            break
    return result

def get_filedata(shasum):
    """Gives the contents of said shasum"""
    #TODO: implement
    pass

def _get_local_file(filename):
    """Returns the file data from the file."""
    filedata = None
    filename = str(filename)
    if exists(abspath(filename)):
        filedata = open(abspath(filename), 'r').read()
    else:
        LOG.error("No file found at " + filename)
    return filedata
        
COMMAND_DICT = {
    'get filedata': get_filedata
}

# vim: set tabstop=4 expandtab textwidth=66 foldmethod=indent: #
