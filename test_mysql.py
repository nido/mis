#!/usr/bin/env python
"""This unit tests the mis mysql module. It is a wrapper around
the real mysql databse and thus this should also test the database
itself."""
from unittest import TestCase
from unittest import main

from config import get_config
from mysql import _get_connection

from mysql import save_container
from mysql import file_exists
from mysql import save_file

TEST_DIRECTORY = 'testfiles'
TEST_FILE = 'testfiles/out.mp4'

MOCK_STREAMCOUNT = 1
MOCK_CONTAINER_TYPE = 'mpegts'
MOCK_DURATION = 1337
MOCK_SIZE = 1048576
MOCK_BITRATE = 131072

def _count_files():
    """counts the number of files"""
    cursor = _get_connection().cursor()
    mysql_string = 'select * from files;'
    result = cursor.execute(mysql_string)
    cursor.close()
    return result

def _count_containers():
    """counts the number of containers"""
    cursor = _get_connection().cursor()
    mysql_string = 'select * from containers;'
    result = cursor.execute(mysql_string)
    cursor.close()
    return result

class TestMysqlModule(TestCase): # pylint: disable-msg=R0904
    """Tests the mysql module in mis"""
    def setUp(self): # pylint: disable-msg=C0103
        """reinitialises the test database"""
        config = get_config()
        # Use the correct database
        # Suggestions for something better are welcome
        config.set('mysql', 'host',
                config.get('mysql_debug', 'host'))
        config.set('mysql', 'database',
                config.get('mysql_debug', 'database'))
        config.set('mysql', 'user',
                config.get('mysql_debug', 'user'))
        config.set('mysql', 'password',
                config.get('mysql_debug', 'password'))
        cursor = _get_connection().cursor()
        # empty the database
        mysql_string = 'delete from files; delete from containers;'
        cursor.execute(mysql_string)

        cursor.close()

    def test_file_exists(self):
        """Tests if a file exists in the database.  No matter
what, filenames should always start with the root (/ or
[driveletter]:/)"""
        result = file_exists('filename')
        self.assertFalse(result)

        save_file('false data', '/new/file/name')
        result = file_exists('/new/file/name')
        self.assertTrue(result)


    def test_save_file(self):
        """Tests if the save_file function works"""
        no_files = _count_files()
        save_file('false data', '/new/file/name')
        no_files_2 = _count_files()
        #todo: extend tests
        #save_file(sha, filename, active=True,
        #        nodename=node(), container_id = None)

        # We added one file, so there should be one more file
        self.assertTrue(no_files_2 - no_files == 1)
    
    def test_save_container(self):
        """Tests the save container function"""
        no_containers = _count_containers()
        save_container(MOCK_STREAMCOUNT, MOCK_CONTAINER_TYPE,
                MOCK_DURATION, MOCK_SIZE, MOCK_BITRATE)
        no_containers_2 = _count_containers()
        self.assertTrue(no_containers_2 - no_containers == 1)

# TODO: I need a more proper test database for this one
#    def test_find_container(self):
#        find_container(nodename, path)

if __name__ == '__main__':
    main()

# vim: set tabstop=4 expandtab textwidth=66: #
