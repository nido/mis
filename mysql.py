from MySQLdb import connect

connection = connect(host='localhost', user='mis', passwd='password', db='mis');

def test_if_in_database(filename):
	mysql_filename = connection.escape(filename)
	mysql_string = "select active from files where path = " + mysql_filename + ";"
	cursor = connection.cursor()
	results = cursor.execute(mysql_string)
	cursor.close()
	if results == 0:
		return False
	return True

def insert_into_database(sha, filename, active=True):
	mysql_filename = connection.escape(filename)
	sql_string = "insert into files (path, sha512, active) values (" + mysql_filename + ", '" + sha + "', " + active.__str__() + ");"
	cursor = connection.cursor()
	results = cursor.execute(sql_string)
	if results == 0:
		return False
	return True
#        FILE=`echo "$1" | sed "s/'/\\\\'/g" | sed 's/"/\\"/g'`
#        SHA512=`sha512sum "$1" | grep -Go "^[^ ]*"`
#echo sha $SHA512
#	echo "insert into files (sha512, path, active) values ('$SHA512', '$FILE', True);" #| mysql -u mis -Ppassword mis
