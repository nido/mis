"""Handles couchdb for mis"""
from socket import socket as network_socket
from socket import error as socketerror
from socket import AF_INET
from socket import SOCK_STREAM

from logging import getLogger
from couchdb.client import Server
from couchdb.client import ResourceNotFound
from platform import node as platform_node
from getpass import getuser

from config import get_config

LOG = getLogger("mis.database")
CONFIG = get_config()

def test_tcp_connection(hostname, port):
    """tests whether the couchdb is listening"""
    result = True
    try:
        test_socket = network_socket(AF_INET, SOCK_STREAM)
        test_socket.connect((hostname, port))
        test_socket.close()
    except socketerror:
        result = False
    return result
        

class DatabaseError(Exception):
    """Error signifying something is wrong with the database"""
    def __init__(self, value):
        """initialises the error"""
        Exception.__init__(self, value)
        self.value = value
        LOG.debug('DatabaseError generated: ' + value)
    def __str__(self):
        """returns the string representation of the error"""
        return repr(self.value)

class Database():
    """The Database class incorperates functions you wish to ask
    the database"""

    jsdir = CONFIG.get('couchdb', 'javascript_directory')

    __DESIGN_VIEWS_PATHS_MAP = \
            file(jsdir + '/design_views_paths_map.js').read()
    __DESIGN_VIEWS_SHASUMS_MAP = \
            file(jsdir + '/design_views_shasums_map.js').read()
    __DESIGN_VIEWS_FORMATS_MAP = \
            file(jsdir + '/design_views_formats_map.js').read()
    __DESIGN_VIEWS_FORMATS_REDUCE = '_sum'
    __DESIGN_VIEWS_SOUND_MAP = \
            file(jsdir + '/design_views_sound_map.js').read()
    __DESIGN_VIEWS_VIDEO_MAP = \
            file(jsdir + '/design_views_sound_map.js').read()
    __DESIGN_FULLTEXT_ARTIST_INDEX = \
            file(jsdir + '/design_fulltext_artist_index.js').read()
    __DESIGN_FULLTEXT_EVERYTHING_INDEX = \
            file(jsdir + '/design_fulltext_artist_index.js').read()

    def create_views(self):
        """creates views and saves them to the database"""
        LOG.info('creating views')
        views = { '_id': '_design/views',
            'language': 'javascript',
            'views': {
                'shasums':
                    {'map': self.__DESIGN_VIEWS_SHASUMS_MAP},
                'paths':
                    {'map': self.__DESIGN_VIEWS_PATHS_MAP },
                'formats':
                    {'map': self.__DESIGN_VIEWS_FORMATS_MAP,
                    'reduce':self.__DESIGN_VIEWS_FORMATS_REDUCE},
                'sound': {'map': self.__DESIGN_VIEWS_SOUND_MAP},
                'video': {'map': self.__DESIGN_VIEWS_VIDEO_MAP}
            },
            'fulltext': {
                'artist':
                    {'index': self.__DESIGN_FULLTEXT_ARTIST_INDEX},
                'everything':
                    {'index': self.__DESIGN_FULLTEXT_EVERYTHING_INDEX}
            }
        }
        self.database.create(views)

    def __init__(self):
        """Initialises a new connection to couch and
        creates a new mis databse if nonexistent"""
        LOG.info('initialising database')
        database_name = CONFIG.get('couchdb', 'database')
        host = CONFIG.get('couchdb', 'hostname')
        port = CONFIG.get('couchdb', 'port')
        database_uri = 'http://' + host + ':' + port + '/'
        self.server = Server(database_uri)
        try:
            # This statement appears to do nothing, but is used to
            # make sure the database is reachable.
            self.server.version
        except AttributeError as error:
            if not test_tcp_connection(host, int(port)):
                LOG.critical("couchdb cannot be reached at " + database_uri)
                exit(1)
            else:
                LOG.error('unknown AttributeError thrown')
                raise error
        try:
            LOG.debug('opening database')
            self.database = self.server[database_name]
        except(ResourceNotFound):
            LOG.info('creating database')
            # The database didn't exist. Lets create it.
            self.database = self.server.create(database_name)
            self.create_views()

    def iterate_all_files(self):
        """With a big database, this is probably a bad idea. this
iterates through every single document."""
        for entry in self.database:
            yield(entry)

    def get_document(self, shasum):
        """extracts a (full) document from the database using the
shasum as an identifier"""
        assert shasum != None
        assert shasum != ''
        LOG.debug('getting document')
        result = None
        try:
            result = self.database[shasum]
            # make sure it actually exists
            
        except (ResourceNotFound) as error:
            LOG.error("don't have that document, doesn't exist:" +
                    str(error))
        return result

    def add_userdata(self, shasum, data):
        """Adds userdata to the database shasum"""
        LOG.debug('add userdata')
        shasum = unicode(shasum)
        user = getuser()
        node = platform_node()
        user_key = node + ':' + user
        userdata = {}
        if not self.file_exists(shasum):
            LOG.error('trying to add userdata to nonexistent file' + shasum)
            return None
        entry = self.database[shasum]
        userdatalist = {} 
        if entry.has_key('userdata'):
            userdatalist = entry['userdata']
        if userdatalist.has_key(user_key):
            userdata = userdatalist[user_key]
        userdata.update(data)
        userdatalist[user_key] = userdata
        entry['userdata'] = userdatalist
        self.database[shasum] = entry

    def add_data(self, shasum, name, data):
        """adds data to a record"""
        assert shasum != None
        shasum = unicode(shasum)
        name = unicode(name)
        LOG.debug('adding data')
        if self.file_exists(shasum):
            mis_file = self.database[shasum]
            if not mis_file.has_key(name) or mis_file[name] != data:
                LOG.info(shasum + " info " + name + " has changed, updating")
                mis_file[name] = data
                self.database[shasum] = mis_file
        else: # create when nonexistent
            LOG.info(shasum + " info " + name + " added")
            entry = {'_id': shasum, name: data}
            self.database.create(entry)

    def add_path(self, shasum, node, path):
        """Adds a path to the database"""
        assert shasum != None
        shasum = unicode(shasum)
        node = unicode(node)
        path = unicode(path)
        LOG.debug('adding path ' + path + " to " + shasum)
        path_info = {'node': node, 'path': path}
        if self.file_exists(shasum):
            mis_file = self.database[shasum]
            mis_file['paths'].append(path_info)
            self.database[mis_file['_id']] = mis_file
        else: # create when nonexistent
            entry = {'_id': shasum, 'paths': [path_info]}
            self.database.create(entry)

    def file_exists(self, shasum):
        """Checks if a file (shasum) exists in the database, and
        returns the entry when found"""
        assert shasum != None
        shasum = unicode(shasum)
        result = None
        LOG.debug('checking if file exists: ' + shasum)
        try:
            # Note: the following line triggers the
            # ResourceNotFound if the sha is not known, this is
            # the way we catch whether it exists.
            self.database[shasum]  # pylint: disable-msg=W0104
            result = shasum
        except ResourceNotFound:
            LOG.debug('trying to find nonexistent entry ' + shasum)
        return result

    def path_exists(self, path, node=None):
        """Checks whether a certain path exists and returns True
        or False"""
        if (node == None):
            node = platform_node
        node = unicode(node)
        path = unicode(path)
        LOG.debug('path exists: ' + node + ':' + path)
        result = None
        key = [node, path]
        results = self.database.view('views/paths', key = key)
        if(len(results) > 0):
            result = results.rows[0]['value']
        return result
		
# vim: set tabstop=4 expandtab textwidth=66: #
