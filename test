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
	else
		echo "analyser $1"
		$1 $2 *.py
	fi


}

for x in test_*.py; do
	python $x
done

analyser pylint "-r n"
analyser epylint
analyser pyflakes
# vim: set tabstop=4 expandtab textwidth=66: #
