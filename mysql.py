"""mysql.py manages everything related to the database.

that is, until we decide we want to support other databases."""
from MySQLdb import connect
from logging import getLogger

from config import get_config
from platform import node

LOG = getLogger('mis.mysql')

CONNECTION = None

def _get_connection():
    """returns the connection"""
    global CONNECTION # pylint: disable-msg=W0603
    if CONNECTION == None:
        CONNECTION = connect(
                host=get_config().get('mysql', 'host'),
                user=get_config().get('mysql', 'user'),
                passwd=get_config().get('mysql', 'password'),
                db=get_config().get('mysql', 'database')
        )
    return CONNECTION


def file_exists(filename):
    """Tests if the filename is known in the database"""
    mysql_filename = _get_connection().escape(filename)
    mysql_string = "select active from files where path = " + \
            mysql_filename + ";"
    cursor = _get_connection().cursor()
    results = cursor.execute(mysql_string)
    cursor.close()
    if results == 0:
        return False
    return True

def save_file(sha, filename, active=True,
        nodename=node(), container_id = None):
    """Inserts a data tuple into the database"""
    mysql_filename = _get_connection().escape(filename)
    mysql_node = _get_connection().escape(nodename)
    if container_id == None:
        mysql_container_id = 'null'
    else:
        mysql_container_id = str(int(container_id))
    sql_string = "insert into files (path, sha512, active, " + \
            "node, container) values (" + mysql_filename + ", '" + sha + \
            "', " + active.__str__() + ", " + mysql_node + \
            ", " + mysql_container_id + ");"
    LOG.debug(sql_string)
    cursor = _get_connection().cursor()
    results = cursor.execute(sql_string)
    if results == 0:
        return False
    return True

def _find_container_by_id(container_id):
    """returns a list of container properties"""
    mysql_container_id = str(int(container_id))
    sql_string = "select * from containers where id = " + \
            mysql_container_id + ";"
    LOG.debug(sql_string)
    cursor = _get_connection().cursor()
    result = cursor.execute(sql_string)
    if result == 0:
        return None
    assert(result == 1)
    return cursor.fetchone()
    

def find_container(nodename, path):
    """returns the container id using a path and node id as input. None if
not found"""
    mysql_path = _get_connection().escape(path)
    mysql_node = _get_connection().escape(nodename)

    sql_string = "select container from files where path = " + \
            mysql_path + " and node = " + mysql_node +";"
    LOG.debug(sql_string)
    cursor = _get_connection().cursor()
    result = cursor.execute(sql_string)
    if result == 0:
        return None
    assert(result == 1)
    container_id = cursor.fetchone()[0]
    return _find_container_by_id(container_id)
    

def _find_container_id(streamcount, container_type, duration, size,
        bitrate):
    """Finds the key for the container with those specific
values. It returns the last added container with these properties.
This also means the save_container function is NOT thread save and
can only be executed once at a time no mitigate potential problems
with this function's behaviour."""
    mysql_streamcount = str(int(streamcount))
    mysql_container_type = _get_connection().escape(container_type)
    if duration != None:
        mysql_duration = str(int(duration))
    else:
        mysql_duration = 'null'
    mysql_size = str(int(size))
    mysql_bitrate = str(int(bitrate))

    sql_string = "select id from containers where streamcount = " \
            + mysql_streamcount + " and container_type = " + \
            mysql_container_type + "and duration_usec = " + \
            mysql_duration + " and size = " + \
            mysql_size + " and bitrate = " + \
            mysql_bitrate + " order by id desc;"

    cursor = _get_connection().cursor()
    results = cursor.execute(sql_string)
    if results == 0:
        return None
    # fetch the highest id (= last addition)
    return cursor.fetchone()[0]

def save_container(streamcount, container_type, duration, size,
        bitrate):
    """Saves the container in the database. is not thread safe"""
    mysql_streamcount = str(int(streamcount))
    mysql_container_type = _get_connection().escape(container_type)
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

    cursor = _get_connection().cursor()
    results = cursor.execute(sql_string)
    if results == 0:
        return None

    container_id = _find_container_id(streamcount, container_type,
            duration, size, bitrate)
    return container_id

# vim: set tabstop=4 expandtab textwidth=66: #
