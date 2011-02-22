function initiate_database(){
	server=$1
	database=$2
	user=$3
	pass=$4
	echo "create database $database;"
	echo "grant select, insert, delete on ${database}.* to '${user}'@'${server}' identified by '${pass}';"
	echo "flush privileges;"
}

table_sql=`cat<<EOF
create table if not exists containers (
	id int not null auto_increment, -- many containers may look the same
	streamcount tinyint not null,
	container_type char(32) not null, -- what most people would call file type, probably
	duration_usec int null,
	size int not null,
	bitrate mediumint not null,
	primary key (id),
	index (duration_usec)
);

create table if not exists files (
	id int not null auto_increment,
	sha512 char(129) not null,
	path varchar(255) not null,
	active boolean not null default True,
	node varchar(64) not null default '.',
	container int null default null,
	source varchar(255) null, -- in case it is known what it is coded from
	primary key (id),
	foreign key (container) references containers(id) ON DELETE set null,
	fulltext index (path),
	index (node)
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
	index (duration_usec)
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
	index (duration_usec)
);
EOF`

if test -z "$4"
then
echo "This program creates the mis database. IT takes 4 arguments"
echo "server, database, user, pass. No defaults are set in this script"
echo "the default server (according to the default config) is localhost"
echo "The production database default name is mis"
echo "the test/debug database default name is mis_test"
echo "the default username is mis"
echo "the default password is password"
echo "please run this script as: $0 servername databasename username password"
echo
echo "oh yea, we try to log in as the root user on mysql to get this to work"
echo "if it doesn't we'll just spit sql for you to execute."
else
echo `initiate_database $1 $2 $3 $4 ` | mysql -h $1 -U root || echo `initiate_database $1 $2 $3 $4 `
echo "$table_sql" | mysql -h $1 -U root -D $2 || echo "use $2; $table_sql"
echo "-- couldn't insert sql code, please run it yourself"
fi
