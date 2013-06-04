AC_INIT([mis],[0.0.1], [nido@foxserver.be], [], [https://github.com/nido/mis])

AM_INIT_AUTOMAKE([foreign])
#AC_CONFIG_MACRO_DIR([m4])

AM_PATH_PYTHON([2.5])
AX_PYTHON_MODULE([couchdb], [need python-couchdb])

AC_CHECK_PROG([FFPROBE], [ffprobe], [ffprobe],
    [AC_MSG_ERROR([Need ffprobe.])]
)

couchdbdir="${libdir}/${PACKAGE}"
AC_SUBST(couchdbdir)

AC_CONFIG_FILES([Makefile mis.spec])

AC_OUTPUT
