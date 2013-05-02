bin_SCRIPTS = mis
mis_PYTHON = python/commands.py python/config.py python/consoleinput.py python/database.py python/ffprobe.py python/log.py python/network.py python/pathwalker.py python/test_commands.py python/test_network.py python/main.py

dist_couchdb_DATA = javascript/design_fulltext_artist_index.js javascript/design_views_paths_map.js javascript/design_views_video_map.js javascript/design_fulltext_everything_index.js javascript/design_views_shasums_map.js javascript/design_views_formats_map.js javascript/design_views_sound_map.js
sysconf_DATA = mis.conf
dist_noinst_DATA = mis.in mis.spec.in

rpm: mis-0.0.1-1.fc18.x86_64.rpm

mis-0.0.1-1.fc18.x86_64.rpm: mis.spec dist-gzip
	mkdir -p $(HOME)/rpmbuild/SOURCES/
	cp $(distdir).tar.gz $(HOME)/rpmbuild/SOURCES/
	rpmbuild -ba $<
	cp $(HOME)/rpmbuild/RPMS/x86_64/$@ $@

python/__init__.py:
	touch $@

mis:
	echo '#!/usr/bin/env python' > $@
	echo 'from mis.main import main' >> $@
	echo 'main()' >> $@

.in.conf:
	cat $< | sed "s#@jsdir@#$(couchdbdir)#g" > $@

pychecker: $(mis_PYTHON)
	cd python && pychecker --only *.py

pylint: $(mis_PYTHON)
	cd python && pylint --disable=W0511 *.py

pyflakes:$(mis_PYTHON)
	pyflakes $<

doxygen: $(mis_PYTHON)
	doxygen

misdir = $(pyexecdir)/mis
couchdbdir = @couchdbdir@

DISTCLEANFILES = mis.conf mis.spec
