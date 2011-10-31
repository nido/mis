#!/usr/bin/env python
"""This unit tests the mis mysql module. It is a wrapper around
the real mysql databse and thus this should also test the database
itself."""
from unittest import TestCase
from unittest import main

from commands import get_function
from commands import get_command
from commands import get_local_file
from log import init_logging

def invalid_function():
    pass

class TestCommandModule(TestCase): # pylint: disable-msg=R0904
    """tests command.py"""

    def setUp(self): # pylint: disable-msg=C0103
        init_logging()

    def test_get_function(self):
        """tests if the get_function method works"""
        command_string = "get filedatabla"
        # get a valid function
        self.assertEqual(get_function(command_string),
                (get_local_file, "bla"))
        # get an invalid function
        self.assertEqual(get_function('invalid command'), None)

    def test_get_command(self):
        """tests if the get_command method works"""
        command_string = "get filedata"
        # get an existing command
        self.assertEqual(get_command(get_local_file),
                command_string)
        # get an illegal command
        self.assertEqual(get_command(invalid_function), None)

#    def test_get_local_file(self):
#        """tests if the get_local_file method works"""

if __name__ == '__main__':
    main()

# vim: set tabstop=4 expandtab textwidth=66: #
