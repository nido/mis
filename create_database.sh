#!/bin/bash

function initiate_database(){
	database="$1"
	echo "create database $database;"
}

function allow_user(){
	server="$1"
	database="$2"
	user="$3"
	pass="$4"
	echo "grant select, insert, delete on ${database}.* to '${user}'@'${server}' identified by '${pass}';"
	echo "flush privileges;"
}

function process(){
	sql_string="$1"
	echo "$sql_string" | mysql -u root || echo "$sql_string"
}
function process_db(){
	database="$1"
	sql_string="$2"
	echo "$sql_string" | mysql -u root $1 2>/dev/null || echo "$sql_string"
}

table_sql=`cat<<EOF
create table if not exists containers (
	id int not null auto_increment,
	streamcount tinyint not null,
	container_type char(32) not null,
	duration_usec int null,
	size int not null,
	bitrate mediumint not null,
	primary key (id),
	index (duration_usec),
	last_modified timestamp default current_timestamp on update current_timestamp
);

create table if not exists files (
	id int not null auto_increment,
	sha512 char(129) not null,
	path varchar(255) not null,
	active boolean not null default True,
	node varchar(64) not null default '.',
	container int null default null,
	source varchar(255) null, -- should it be known what it is coded from
	primary key (id),
	foreign key (container) references containers(id) ON DELETE set null,
	fulltext index (path),
	index (node),
	last_modified timestamp default current_timestamp on update current_timestamp
);

create table if not exists video_streams (
	id int not null auto_increment,
	container int not null,
	entry tinyint not null,
	codec char(16) not null,
	width smallint not null,
	height smallint not null,
	display_aspect float not null,
	framerate float not null,
	duration_usec mediumint null,
	bitrate mediumint null,
	primary key(id),
	foreign key (container) references containers(id) on delete cascade,
	index (duration_usec),
	last_modified timestamp default current_timestamp on update current_timestamp
);

create table if not exists audio_streams (
	id int not null auto_increment,
	container int not null,
	entry tinyint not null,
	codec char(4) not null,
	samplerate tinyint not null,
	channels tinyint not null,
	duration_usec mediumint null,
	primary key (id),
	foreign key (container) references containers(id) on delete cascade,
	index (duration_usec),
	last_modified timestamp default current_timestamp on update current_timestamp
);
EOF`

if test -z "$3"
then
	echo "This program creates the mis database. IT takes 3 arguments"
	echo "server, user, pass. No defaults are set in this script"
	echo "default user is mis"
	echo "the default password is password"
	echo "the servername is where is connected from, usually localhost"
	echo "sorry for the confusion, better ideas are welcome"
	echo "please run this script as: $0 servername username password"
	echo
	echo "oh yea, we try to log in locally as the root user on mysql to get this to work"
	echo "if it doesn't we'll just spit sql for you to execute."
else
	servername=$1
	username=$2
	password=$3
	process "`initiate_database mis`"
	process "`initiate_database mis_test`"
	process_db mis "$table_sql"
	process_db mis_test "$table_sql"
	allow_user $servername mis $user $password
	allow_user $serverame mis_test $user $password
	process "-- couldn't insert sql code, please run it yourself"
fi
