""" temp class for raw input"""

from commands import get_function

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
            
class Console:
    """Class for inputting commands into mis directly."""
    def __init__(self):
        """create the class"""
        print "Media Information System - Console"

    def attach(self):
        """emulated 'attaching'. basically, it just asks input and
executes it in a while(true) loop"""
        while(True):
            print ""
            text = raw_input('# ')
            args = text.split(' ', 1)
            command = args[0]
            argument = None
            if len(args) == 2:
                argument = args[1]
            function = get_function(command)
            if function:
                x = function(argument)
                print(x)
            else:
                print "Invalid command: " + text

# vim: set tabstop=4 shiftwidth=4 expandtab textwidth=66 foldmethod=indent: #
