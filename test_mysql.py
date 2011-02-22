#!/usr/bin/env python
"""This unit tests the mis mysql module. It is a wrapper around
the real mysql databse and thus this should also test the database
itself."""
from unittest import TestCase
from unittest import main

from config import get_config
from mysql import get_connection

from mysql import file_exists
from mysql import save_file
TEST_DIRECTORY = 'testfiles'
TEST_FILE = 'testfiles/out.mp4'

def _count_files():
    """counts the number of files"""
    cursor = get_connection().cursor()
    mysql_string = 'select * from files;'
    result = cursor.execute(mysql_string)
    cursor.close()
    return result

class TestMysqlModule(TestCase): # pylint: disable-msg=R0904
    """Tests the mysql module in mis"""
    def setUp(self): # pylint: disable-msg=C0103
        """reinitialises the test database"""
        config = get_config()
        # Use the correct database
        config.set('mysql', 'host',
                config.get('mysql_debug', 'host'))
        config.set('mysql', 'database',
                config.get('mysql_debug', 'database'))
        config.set('mysql', 'user',
                config.get('mysql_debug', 'user'))
        config.set('mysql', 'password',
                config.get('mysql_debug', 'password'))
        cursor = get_connection().cursor()
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

        # We added one file, so there should be one more file
        self.assertTrue(no_files_2 - no_files == 1)
   
if __name__ == '__main__':
    main()
#suite =unittest.TestLoader().loadTestsFromTestCase(TestMysqlModule)
#unittest.TextTestRunner(verbosity=2).run(suite)

# vim: set tabstop=4 expandtab textwidth=66: #
