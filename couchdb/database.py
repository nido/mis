"""Handles couchdb for mis"""

from couchdb.client import Server
from couchdb.client import ResourceNotFound

def template_replace(template, replace):
        function = template
        for key in replace:
            value = replace[key]
            function = function.replace('{{' + key + '}}', value)
        return function

class Database():
    """The Database class incorperates functions you wish to ask
    the database"""

    __PATH_EXISTS_TEMPLATE = """function(doc) {
  for (i=0; i<doc.paths.length; i++){
    entry = doc.paths[i]
    if (entry.node == "{{node}}" && entry.path == "{{path}}"){
      emit(doc);
    }
  }
}"""

    __FILE_EXISTS_TEMPLATE = """function(doc) {
  if(doc.sha512 == "{{sha512}}"){
    emit(doc._id, doc)
  }
}"""

    def __init__(self):
        """Initialises a new connection to couch and
        creates a new mis databse if nonexistent"""
        self.server = Server()
        try:
            self.database = self.server['mis']
        except(ResourceNotFound):
            self.database = self.server.create('mis')

    def add_path(self, shasum, node, path):
        """Adds a path to the database"""
        path_info = {'node': node, 'path': path}
        mis_file = self.file_exists(shasum)
        if mis_file:
            mis_file['paths'].append(path_info)
            self.database[mis_file['_id']] = mis_file
        else:
            entry = {'sha512':shasum, 'paths':[path_info]}
            self.database.create(entry)

    def file_exists(self, sha512):
        """Checks if a file (shasum) exists in the database, and
        returns the entry when found"""
        result = None
        entries = {'sha512': sha512}
        function = template_replace(self.__FILE_EXISTS_TEMPLATE, entries)
        results = self.database.query(function)
        if len(results) > 0:
            result = (results.rows[0].value)
        return result

    def path_exists(self, node, path):
        """Checks whether a certain path exists and returns True
        or False"""
        result = False
        entries = {'path':path, 'node':node}
        function = template_replace(self.__PATH_EXISTS_TEMPLATE, entries)
        results = self.database.query(function)
        if len(results) > 0:
            result = True
        return result
		
# vim: set tabstop=4 expandtab textwidth=66: #
