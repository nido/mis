#!/bin/bash

function exists(){
	test -f "`which $1 2>/dev/null`"
}

function analyser(){
	if ! exists $1
	then
		echo "you should install pyflakes, or put it in your path"
	else
		echo "analyser $1"
		$1 $2 *.py
	fi


}

analyser pylint "-r n"
analyser epylint
analyser pyflakes
