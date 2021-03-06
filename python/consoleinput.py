""" temp class for raw input"""

from commands import get_function
from database import Database


def batch_update():
    """does a batch update through the console"""
    database = Database()
    meatware = Consoleinput()
    meatware.get_fieldnames()
    for entry in database.iterate_all_files():
        if len(entry) == 128:
            userdict = meatware.input_data()
            database.add_userdata(entry, userdict)


class Consoleinput:
    """class holding it"""
    def __init__(self):
        self.fields = []

    def get_fieldnames(self):
        """Asks you to define fields"""
        print "Please type a space-separated list of properties"
        print "e.g.: name location whatever"
        string = raw_input()
        self.fields = string.split(" ")

    def input_data(self):
        """returns values put in for they keys given in fieldnames"""
        result = {}
        for field in self.fields:
            print "Please enter value for " + field
            answer = raw_input()
            result[field] = answer
        return result


def console():
    """function for inputting commands into mis directly."""
    print "Media Information System - Console"
    print "type help for help"
    value = True
    while(value):
        print ""
        text = raw_input('# ')
        argument = None
        if text == 'exit':
            command = None
            value = False
        elif text == 'batch':
            batch_update()
        else:
            command = get_function(text)
            if command is None:
                print "Invalid command: " + text
                continue
            (function, argument) = get_function(text)
            result = function(argument[1:])
            if result is not None:
                print(result)
        if text == 'help':  # add 'exit' to the list hack
            print 'exit: exit the program'

# vim: set tabstop=4 shiftwidth=4 expandtab textwidth=66 foldmethod=indent: #
