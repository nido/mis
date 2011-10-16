"""Handles couchdb for mis"""

from datetime import datetime

from couchdb.client import Server
from couchdb.client import ResourceNotFound

class Database():

    _PATH_EXISTS_TEMPLATE = """function(doc) {
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
        self.server = Server()
        try:
            self.database = self.server['mis']
        except(ResourceNotFound):
            self.database = self.server.create('mis')

    def add_path(self, shasum, path_info):
        mis_file = self.file_exists(shasum)
        if mis_file:
            mis_file['paths'].append(path_info)
            self.database[mis_file['_id']] = mis_file
        else:
            entry = {'sha512':shasum, 'paths':[path_info]}
            self.database.create(entry)

    def file_exists(self, sha512):
        result = None
        function = self.__FILE_EXISTS_TEMPLATE
        function = function.replace('{{sha512}}', sha512)
        results = self.database.query(function)
        if len(results) > 0:
            result = (results.rows[0].value)
        return result

    def path_exists(self, node, path):
        result = False
        function = self._PATH_EXISTS_TEMPLATE
        function = function.replace('{{path}}', path)
        function = function.replace('{{node}}', node)
        results = self.database.query(function)
        if len(results) > 0:
            result = True
        return result
		
# vim: set tabstop=4 expandtab textwidth=66: #
