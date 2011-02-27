#!/bin/bash
# simple script generating the loglevel defaults creation in python. For devs only
cat *.py | grep -Go "'mis\.[^']*'" | sort | uniq | while read line; do echo "    config.set($line, 'info')"; done
