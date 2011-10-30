""" temp class for raw input"""
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
            
# vim: set tabstop=4 shiftwidth=4 expandtab textwidth=66 foldmethod=indent: #
