#!/bin/bash

function exists(){
	test -f "`which $1 2>/dev/null`"
}
if ! exists pyflakes
then
echo "you should install pyflakes, or put it in your path"
else
pyflakes *.py
fi

if ! exists pylint
then
echo "you should install pylint, or put it in your path"
else
echo "When using python 2.7, expect an error on hashlib. Any"
echo "suggestions on how to deal with it appreciated."
pylint -r n *.py
fi

