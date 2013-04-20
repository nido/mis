mis_PYTHON = python/commands.py python/config.py python/consoleinput.py python/database.py python/ffprobe.py python/log.py python/main.py python/network.py python/pathwalker.py python/test_commands.py python/test_network.py

couchdb_DATA = javascript/design_fulltext_artist_index.js javascript/design_views_paths_map.js javascript/design_views_video_map.js javascript/design_fulltext_everything_index.js javascript/design_views_shasums_map.js javascript/design_views_formats_map.js javascript/design_views_sound_map.js

doxygen: $(mis_PYTHON)
	doxygen

misdir = $(pythondir)/mis
couchdbdir = $(libdir)/$(PACKAGE)
