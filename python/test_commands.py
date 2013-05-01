#!/usr/bin/env python
"""This unit tests the mis mysql module. It is a wrapper around
the real mysql databse and thus this should also test the database
itself."""
from unittest import TestCase
from unittest import main

from commands import get_function
from commands import get_command
from commands import get_filedata
from commands import _get_local_file
from log import init_logging
from pathwalker import Pathwalker

def invalid_function():
    """no good function that does nothing"""
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
                get_filedata)
        # get an invalid function
        self.assertEqual(get_function('invalid command'), None)

    def test_get_command(self):
        """tests if the get_command method works"""
        command_string = "get filedata"
        # get an existing command
        self.assertEqual(get_command(get_filedata),
                command_string)
        # get an illegal command
        self.assertEqual(get_command(invalid_function), None)

    def test_get_filedata(self):
        """Tests the filedata extractor"""
        # get check data
        filedata = file('../test_files/test.avi').read()
        from hashlib import sha512 # pylint: disable-msg=E0611
        shasum = sha512(filedata).hexdigest()
        # add to database
        Pathwalker().evaluate_path('../test_files')
        self.assertEqual(get_filedata(shasum), filedata)
        # text nonexistent file fetch
        self.assertEqual(get_filedata('invalid_doc'), None)

    def test__get_local_file(self):
        """Tests if _get_local_file works correctly"""
        filedata = file('../test_files/test.avi').read()
        test = _get_local_file('../test_files/test.avi')
        self.assertEqual(test, filedata)
        # text nonexistent file
        self.assertEqual(_get_local_file(''), None)

if __name__ == '__main__':
    main()

# vim: set tabstop=4 expandtab textwidth=66: #
