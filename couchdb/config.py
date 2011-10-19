"""config is responsible for configuration

configuration comes in the following flavours, from least to most
precedense: default configuration (whatever is done when not
defined (as in, A: this should be documented behavior, and B: this
program should work without config files ), global configuration 
(what is found in /etc/mis.conf (or
equivalent once one is defined)), user configuration (defined in
~/.mis/config), argument configuration (added at the
command-line). This file is also responsible for parsing these
files.
"""
from ConfigParser import SafeConfigParser
from os.path import expanduser
from ConfigParser import NoSectionError
from logging import getLogger
LOG = getLogger('mis.config')
SINGLETON = None #: Singleton holds the configuration itself.

def get_config():
    """returns the configuration"""
    global SINGLETON # pylint: disable-msg=W0603
    if(SINGLETON == None):
        SINGLETON = Configuration()
    return SINGLETON


def default_config():
    """default config() returns the default configuration. This
function is defined in order to keep the configuration default in
one place for annotation, and also to keep the rest of the program
blissfully ignorant of the defaultness of said configuration."""
    config = SafeConfigParser()
    # Default configurtion settings for the MySQL server
    # network settings
    config.add_section('network')
    config.set('network', 'host', '')
    config.set('network', 'port', '55433')
    # default loglevels
    config.add_section('loglevels')
    config.set('loglevels', 'mis.config', 'info')
    config.set('loglevels', 'mis.ffprobe', 'info')
    config.set('loglevels', 'mis.log', 'info')
    config.set('loglevels', 'mis.main', 'info')
    config.set('loglevels', 'mis.media', 'info')
    config.set('loglevels', 'mis.network', 'info')
    config.set('loglevels', 'mis.network.Server_handler.traffic', 'info')
    config.set('loglevels', 'mis.pathwalker', 'info')
    config.add_section('charsets')
    config.set('charsets', 'filesystem', 'utf8')
    config.set('charsets', 'fallback', 'latin1')

    return config

class Configuration():
    """the configuration itself, dictionary like. We'll be using
python's very own ConfigParser."""
    system_file = '/etc/mis.conf'
    user_filename  = expanduser('~/.mis/config')

    def __init__(self):
        """initialises the configurations"""
        self._parser = default_config()
        self.read = self._parser.read([self.system_file, self.user_filename])
        self.userconfig = SafeConfigParser()
        self.userconfig.read([self.user_filename])
        LOG.info("Configuration initialised")

    def list_section(self, section):
        """returns the entries in a section"""
        result = None
        if self._parser.has_section(section):
            result = self._parser.options(section)
        else:
            LOG.debug("cannot log section " + section + 
                    ", it doesn't exist.")
        return result

    def get(self, section, name):
        """gets a configuration option"""
        result = None
        try:
            result = self._parser.get(section, name)
        except NoSectionError:
            LOG.warn("Section " + section + " doesn't exist.")
        return result
        

    def set(self, section, name, value, permanent=False):
        """sets a configuration option"""
        if (not self._parser.has_section(section)):
            self._parser.add_section(section)
        self._parser.set(section, name, value)
        if(permanent):
            if (not self.userconfig.has_section(section)):
                self.userconfig.add_section(section)
            self.userconfig.set(section, name, value)
            user_file = open(self.user_filename,'w')
            self.userconfig.write(user_file)
            user_file.close()
# vim: set textwidth=66 ts=4 expandtab: #
