"""mysql.py manages everything related to the database.

that is, until we decide we want to support other databases."""
from MySQLdb import connect

CONNECTION = connect(host='localhost', user='mis', passwd='password', db='mis')

from platform import node

def test_if_in_database(filename):
    """Tests if the filename is known in the database"""
    mysql_filename = CONNECTION.escape(filename)
    mysql_string = "select active from files where path = " + \
            mysql_filename + ";"
    cursor = CONNECTION.cursor()
    results = cursor.execute(mysql_string)
    cursor.close()
    if results == 0:
        return False
    return True

def insert_into_database(sha, filename, active=True,
        nodename=node()):
    """Inserts a data tuple into the database"""
    mysql_filename = CONNECTION.escape(filename)
    mysql_node = CONNECTION.escape(nodename)
    sql_string = "insert into files (path, sha512, active, " + \
            "node) values (" + mysql_filename + ", '" + sha + \
            "', " + active.__str__() + ", " + mysql_node + ");"
    cursor = CONNECTION.cursor()
    results = cursor.execute(sql_string)
    if results == 0:
        return False
    return True

# vim: set tabstop=4 expandtab textwidth=66: #
