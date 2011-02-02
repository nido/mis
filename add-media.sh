#!/bin/bash
# This script checks the media directory and adds the new files to the mis.

function evaluate_file(){
        FILE=`echo "$1" | sed "s/'/\\\\'/g" | sed 's/"/\\"/g'`
echo file "$FILE"
        echo "select 1 from files where path like '$FILE'" | mysql mis
        TEST=`echo "select 1 from files where path like '$FILE'" | mysql mis`
test -n "$TEST" && echo test "$TEST"
        test -z "$TEST" && insert_into_database "$1"
}

function insert_into_database(){
echo insertin
        FILE=`echo "$1" | sed "s/'/\\\\'/g" | sed 's/"/\\"/g'`
        SHA512=`sha512sum "$1" | grep -Go "^[^ ]*"`
        echo "insert into files values('$SHA512', '$FILE', true);" | mysql mis
}

find /var/data/media/video -type f | while read line; do evaluate_file "$line"; done
