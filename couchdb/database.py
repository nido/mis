"""Handles couchdb for mis"""

from logging import getLogger
from couchdb.client import Server
from couchdb.client import ResourceNotFound

from config import get_config

LOG = getLogger("mis.database")

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
      key = [entry.node, entry.path]
      if(entry.node && entry.path){
        emit(key, doc._id)
      }
  }
}"""

    __DESIGN_VIEWS_SHASUMS_MAP = """function(doc){
    emit(doc._id)
}"""

    __DESIGN_VIEWS_FORMATS_MAP = """function(doc) {
  if(doc.ffprobe.container.format_name){
    emit(doc.ffprobe.container.format_name, 1);
  }
}"""

    __DESIGN_VIEWS_FORMATS_REDUCE = '_sum'

    __DESIGN_VIEWS_MUSIC_MAP = """function(doc) {
  music = ["aac", "ac3", "mp3"];
  for (i=0; i<music.length; i++){
    if(doc.ffprobe.container.format_name == music[i]){
      emit(doc, music[i]);
    }
  }
}"""

    __DESIGN_VIEWS_VIDEO_MAP = """function(doc) {
  video = ["asf", "avi", "flv", "h263", "matroska,webm",
"mov,mp4,m4a,3gp,3g2,mj2", "mpeg"];
  for (i=0; i<video.length; i++){
    if(doc.ffprobe.container.format_name == video[i]){
      emit(doc);
    }
  }
}"""

    __DESIGN_VIEWS_VIDEO_MAP = """function(doc) {
  if(doc.ffprobe.tags.title){
    emit(doc.ffprobe.tags.title);
  } else if(doc.ffprobe.container.filename) {
    emit(doc.ffprobe.container.filename);
  } else {
    emit(doc.paths[0].path)
  }
}"""

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
                'music': {'map': self.__DESIGN_VIEWS_MUSIC_MAP},
                'video': {'map': self.__DESIGN_VIEWS_VIDEO_MAP}
            }
        }
        self.database.create(views)

    def __init__(self):
        """Initialises a new connection to couch and
        creates a new mis databse if nonexistent"""
        database_name = get_config().get('couchdb', 'database')
        host = get_config().get('couchdb', 'hostname')
        port = get_config().get('couchdb', 'port')
        database_uri = 'http://' + host + ':' + port + '/'
        self.server = Server(database_uri)
        try:
            self.database = self.server[database_name]
        except(ResourceNotFound):
            # The database didn't exist. Lets create it.
            self.database = self.server.create(database_name)
            self.create_views()

    def get_document(self, shasum):
        """extracts a (full) document from the database using the
shasum as an identifier"""
        result = None
        try:
            result = self.database[shasum]
        except ResourceNotFound:
            LOG.error("don't have that document, doesn't exist")
        return result

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
            return results.rows[0]['value']
		
# vim: set tabstop=4 expandtab textwidth=66: #
