"""command is the part of the program which parses commands given
to the system and checks authorisation for said commands, and
initiates the appropriate backend command (probably network,
database or maybe probe)"""
from mysql import file_exists


def parse(string):
    """This parses a sting which is supposed to be a command
    get_file_command = 'get_file '
    if string[:len(get_file_command)] == get_file_command:
        result = get_local_file(string[len(get_file_command):]
    return result"
    """
    pass

def get_local_file(filename):
    """Returns the file data from the file."""
    filedata = None
    if file_exists(filename):
        filedata = open(filename).read()
    return filedata
        


# vim: set tabstop=4 expandtab textwidth=66 foldmethod=indent: #
