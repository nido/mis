"""Handles couchdb for mis"""

from logging import getLogger

from couchdb.client import Server
from couchdb.client import ResourceNotFound

LOG = getLogger("mis.couchdb")

def template_replace(template, replace):
    """Takes a template and replaces the the keys in the replace
    fictionary with the values"""
    function = template
    for key in replace:
        value = replace[key]
        function = function.replace('{{' + key + '}}', value)
    return function

class DatabaseError(Exception):
    """Error signifying something is wrong with the database"""
    def __init__(self, value):
        """initialises the error"""
        Exception.__init__(self, value)
        self.value = value
        LOG.debug(value)
    def __str__(self):
        """returns the string representation of the error"""
        return repr(self.value)

class Database():
    """The Database class incorperates functions you wish to ask
    the database"""

    __DESIGN_VIEWS_PATHS_MAP = """function(doc){
  for(i=0; i<doc.paths.length; i++){
      entry = doc.paths[i]
      key = entry.node + ':' + entry.path
      if(entry.node && entry.path){
        emit(key, doc._id)
      }
  }
}"""

    __DESIGN_VIEWS_SHASUMS_MAP = """function(doc){
    emit(doc._id)
}"""

    def __init__(self):
        """Initialises a new connection to couch and
        creates a new mis databse if nonexistent"""
        self.server = Server()
        try:
            self.database = self.server['mis']
        except(ResourceNotFound):
            # The database didn't exist. Lets create it.
            self.database = self.server.create('mis')
            views = {
                '_id': '_design/views',
                'language': 'javascript',
                'views': {
                    'shasums':
                        {'map': self.__DESIGN_VIEWS_SHASUMS_MAP},
                    'paths':
                        {'map': self.__DESIGN_VIEWS_PATHS_MAP }}}
            self.database.create(views)

    def add_data(self, shasum, name, data):
        """adds data to a record"""
        if self.file_exists(shasum):
            mis_file = self.database[shasum]
            mis_file[name] = data
            self.database[shasum] = mis_file
        else: # create when nonexistent
            entry = {'_id': shasum, name: data}
            self.database.create(entry)
            

    def add_path(self, shasum, node, path):
        """Adds a path to the database"""
        path_info = {'node': node, 'path': path}
        if self.file_exists(shasum):
            mis_file = self.database[shasum]
            mis_file['paths'].append(path_info)
            self.database[mis_file['_id']] = mis_file
        else: # create when nonexistent
            entry = {'_id': shasum, 'paths': [path_info]}
            self.database.create(entry)

    def file_exists(self, sha512):
        """Checks if a file (shasum) exists in the database, and
        returns the entry when found"""
        result = False
        try:
            # Note: the following line triggers the
            # ResourceNotFound if the sha is not known
            self.database[sha512]  # pylint: disable-msg=W0104
            result = True
        except ResourceNotFound:
            pass # expected
        return result

    def path_exists(self, node, path):
        """Checks whether a certain path exists and returns True
        or False"""
        result = None
        key = [node, path]
        results = self.database.view('views/paths', key = key)
        if(len(results) > 0):
            return result
		
# vim: set tabstop=4 expandtab textwidth=66: #
