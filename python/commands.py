""" command is the part of the program which parses commands given
    to the system and checks authorisation for said commands, and
    initiates the appropriate backend command (probably network,
    database or maybe probe)"""
from logging import getLogger
from os.path import abspath
from os.path import exists
from os.path import isfile
from os.path import isdir
from platform import node
from pathwalker import Pathwalker

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
            break  # optimisation: breakout of for loop
    if command is None:
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
    result = None
    database = Database()
    document = database.get_document(shasum)
    LOG.debug('get filedata shasum ' + shasum + ' doc: ' +
              str(document))
    if (document is not None) and ('paths' in document):
        for path in document['paths']:
            if (path['node'] == node() and
                    exists(path['path'])):
                result = _get_local_file(path['path'])
                break  # break out of 'for path'
    # TODO: implement network fetch
    return result


def index(path):
    """Indexes a directory"""
    if path is None:
        path = abspath("../test_files")

    if isdir(path):
        walker = Pathwalker()
        walker.evaluate_path(path)
    else:
        LOG.error(path + 'is not a directory')


def _get_local_file(filename):
    """Returns the file data from the file."""
    filedata = None
    filename = str(filename)
    if isfile(abspath(filename)):
        filedata = open(abspath(filename), 'r').read()
    else:
        LOG.error("No file found at " + filename)
    return filedata


def usage(arg=None):  # pylint: disable-msg=W0613
    """echos how to use this executable"""
    if(arg):
        help(arg)
    else:
        print """
batch
    stupid legacy function
help
    display this text.
index [directory]
    indexes the directory, or ../test_files when no argument is
    given and adds it to the couchdb database
readfile path
    returns the content of a file at path
"""


COMMAND_DICT = {
    'get filedata': get_filedata,
    'readfile': _get_local_file,
    'index': index,
    'help': usage
}

# vim: set tabstop=4 expandtab textwidth=66 foldmethod=indent: #
