"""mysql.py manages everything related to the database.

that is, until we decide we want to support other databases."""
from MySQLdb import connect
from logging import getLogger

LOG=getLogger('mis.mysql')

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

def save_file(sha, filename, active=True,
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

def save_container(streamcount, container_type, duration, size,
        bitrate):
    mysql_streamcount = str(int(streamcount))
    mysql_container_type = CONNECTION.escape(container_type)
    if duration != None:
        mysql_duration = str(int(duration))
    else:
        mysql_duration = 'null'
    mysql_size = str(int(size))
    mysql_bitrate = str(int(bitrate))
    
    sql_string = "insert into containers (streamcount, " + \
            "container_type, duration_usec, size, bitrate) " + \
            "values (" + mysql_streamcount + ", " + \
            mysql_container_type + ", " + mysql_duration + ", " +\
            mysql_size + ", " + mysql_bitrate + ");"

    LOG.debug(sql_string)

    cursor = CONNECTION.cursor()
    results = cursor.execute(sql_string)
    if results == 0:
        return False
    return True

# vim: set tabstop=4 expandtab textwidth=66: #
