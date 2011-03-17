#!/bin/bash
# This little program has the responsibility to run any test on
# the code it is able to run. This currently includes pylint,
# pyflakes, epylint and unit tests, however, this is to be
# extended with any other test methods known by anyone.

function exists(){
	test -f "`which $1 2>/dev/null`"
}

function analyser(){
	if ! exists $1
	then
		echo "you should install $1, or put it in your path"
        return false
	else
		echo "analyser $1"
		$1 $2 *.py 2>&1 | grep -v "^[ \t]*$"
	fi


}

for x in test_*.py; do
    MODNAME=`echo $x | sed "s/^test_//" | sed "s/.py$//"`
    if ! exists coverage
    then
        echo "you should install python-coverage, or put coverage in your path"
        CMD=python
    else
        coverage erase
        CMD="coverage run -a --branch"
    fi
	$CMD $x 2>&1 | grep -v "^\(-*\)$"
    if exists coverage
    then
        coverage report | grep "\($MODNAME\|^Name\)"
    fi
done

analyser pylint "-r n" | grep -v "^\([RI]:\|No config file\)"
analyser epylint
analyser pyflakes
if exists coverage 
then
    echo "generating total coverage report"
    coverage erase
    for x in test*.py
    do
        coverage run -a --branch $x
    done
    coverage html
fi
# vim: set tabstop=4 expandtab textwidth=66: #
