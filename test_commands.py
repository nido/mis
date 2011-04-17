#!/usr/bin/env python
"""This unit tests the mis mysql module. It is a wrapper around
the real mysql databse and thus this should also test the database
itself."""
from unittest import TestCase
from unittest import main

from commands import get_function
from commands import get_command
from commands import get_local_file

class TestCommandModule(TestCase): # pylint: disable-msg=R0904
    """tests command.py"""


    def test_get_function(self):
        """tests if the get_function method works"""
        command_string = "get filedatabla"
        self.assertEqual(get_function(command_string),
                (get_local_file, "bla"))

    def test_get_command(self):
        """tests if the get_command method works"""
        command_string = "get filedata"
        self.assertEqual(get_command(get_local_file),
                command_string)

#    def test_get_local_file(self):
#        """tests if the get_local_file method works"""

if __name__ == '__main__':
    main()

# vim: set tabstop=4 expandtab textwidth=66: #
