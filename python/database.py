"""Handles couchdb for mis"""

from logging import getLogger
from couchdb.client import Server
from couchdb.client import ResourceNotFound

from config import get_config
from network import test_tcp_connection

LOG = getLogger("mis.database")
CONFIG = get_config()

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

    __DESIGN_VIEWS_PATHS_MAP = file('../javascript/design_views_paths_map.js').read()
    __DESIGN_VIEWS_SHASUMS_MAP = file('../javascript/design_views_shasums_map.js').read()
    __DESIGN_VIEWS_FORMATS_MAP = file('../javascript/design_views_formats_map.js').read()
    __DESIGN_VIEWS_FORMATS_REDUCE = '_sum'
    __DESIGN_VIEWS_SOUND_MAP = file('../javascript/design_views_sound_map.js').read()
    __DESIGN_VIEWS_VIDEO_MAP = file('../javascript/design_views_sound_map.js').read()
    __DESIGN_FULLTEXT_ARTIST_INDEX = file('../javascript/design_fulltext_artist_index.js').read()
    __DESIGN_FULLTEXT_EVERYTHING_INDEX = file('../javascript/design_fulltext_artist_index.js').read()

    def create_views(self):
        """creates views and saves them to the database"""
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
        database_name = CONFIG.get('couchdb', 'database')
        host = CONFIG.get('couchdb', 'hostname')
        port = CONFIG.get('couchdb', 'port')
        database_uri = 'http://' + host + ':' + port + '/'
        self.server = Server(database_uri)
        try:
            self.server.version
        except AttributeError as error:
            if not test_tcp_connection(host, int(port)):
                LOG.critical("couchdb cannot be reached at " + database_uri)
                exit(1)
            else:
                raise error
        try:
            self.database = self.server[database_name]
        except(ResourceNotFound):
            # The database didn't exist. Lets create it.
            self.database = self.server.create(database_name)
            self.create_views()

    def iterate_all_files(self):
        """With a big database, this is probably a bad idea. Some
yielding thing may be handier for iterating through everything,
but that is a concern for later."""
        # TODO: update for what it says above
        for x in self.database:
            yield(x)

    def get_document(self, shasum):
        """extracts a (full) document from the database using the
shasum as an identifier"""
        result = None
        try:
            result = self.database[shasum]
        except ResourceNotFound:
            LOG.error("don't have that document, doesn't exist")
        return result

    def add_userdata(self, shasum, data):
        shasum = unicode(shasum)
        from getpass import getuser
        user = getuser()
        from platform import node
        node = node()
        user_key = node + ':' + user
        userdata = {}
        if self.file_exists(shasum):
            x = self.database[shasum]
            userdatalist = {} 
            if x.has_key('userdata'):
                userdatalist = x['userdata']
            if userdatalist.has_key(user_key):
                userdata = userdatalist[user_key]
            userdata.update(data)
            userdatalist[user_key] = userdata
            x['userdata'] = userdatalist
            self.database[shasum]=x
            
                
        

    def add_data(self, shasum, name, data):
        """adds data to a record"""
        shasum = unicode(shasum)
        name = unicode(name)
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
        shasum = unicode(shasum)
        node = unicode(node)
        path = unicode(path)
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
        shasum = unicode(shasum)
        result = None
        try:
            # Note: the following line triggers the
            # ResourceNotFound if the sha is not known
            self.database[shasum]  # pylint: disable-msg=W0104
            result = shasum
        except ResourceNotFound:
            pass # expected
        return result

    def path_exists(self, node, path):
        """Checks whether a certain path exists and returns True
        or False"""
        node = unicode(node)
        path = unicode(path)
        result = None
        key = [node, path]
        results = self.database.view('views/paths', key = key)
        if(len(results) > 0):
            result = results.rows[0]['value']
        return result
		
# vim: set tabstop=4 expandtab textwidth=66: #
