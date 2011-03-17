#!/usr/bin/env python
"""This unit tests the mis mysql module. It is a wrapper around
the real mysql databse and thus this should also test the database
itself."""
from unittest import TestCase
from unittest import main

from commands import get_function
#from commands import get_command
from commands import get_local_file

class TestCommandModule(TestCase): # pylint: disable-msg=R0904
    """Tests the commands module in mis"""
    def setUp(self): # pylint: disable-msg=C0103
        pass

    def test_get_function(self):
        """tests the function get_function"""
        guess = get_function('get filedataargument')
        answer = (get_local_file, 'argument')
        self.assertTrue(guess == answer)

if __name__ == '__main__':
    main()

# vim: set tabstop=4 expandtab textwidth=66: #
