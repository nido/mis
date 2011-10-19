"""Handles couchdb for mis"""

from couchdb.client import Server
from couchdb.client import ResourceNotFound

def template_replace(template, replace):
    """Takes a template and replaces the the keys in the replace
    fictionary with the values"""
    function = template
    for key in replace:
        value = replace[key]
        function = function.replace('{{' + key + '}}', value)
    return function

class Database():
    """The Database class incorperates functions you wish to ask
    the database"""

    __DESIGN_VIEWS_PATHS_MAP = """function(doc){
  for(i=0; i<doc.paths.length; i++){
      entry = doc.paths[i]
      key = entry.node + ':' + entry.path
      if(entry.node && entry.path){
        emit(key, doc)
      }
  }
}"""
  

    __DESIGN_VIEWS_SHASUMS_MAP = """function(doc){
    emit(doc._id,doc)
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
        try:
         mis_file = self.file_exists(shasum)
         if mis_file:
            mis_file[name] = data
            self.database[shasum] = mis_file
        except:
            print mis_file
            print name
            print data
            raise

    def add_path(self, shasum, node, path):
        """Adds a path to the database"""
        path_info = {'node': node, 'path': path}
        mis_file = self.file_exists(shasum)
        if mis_file:
            mis_file['paths'].append(path_info)
            self.database[mis_file['_id']] = mis_file
        else:
            entry = {'_id':shasum, 'paths':[path_info]}
            self.database.create(entry)

    def file_exists(self, sha512):
        """Checks if a file (shasum) exists in the database, and
        returns the entry when found"""
        result = None
        results = self.database.view('views/shasums', key = sha512)
        if(len(results) > 0):
            result = results.rows[0].value
        return result

    def path_exists(self, node, path):
        """Checks whether a certain path exists and returns True
        or False"""
        result = False
        key = node + ":" + path
        results = self.database.view('views/paths', key = key)
        if(len(results) > 0):
            result = True
        return result
		
# vim: set tabstop=4 expandtab textwidth=66: #
