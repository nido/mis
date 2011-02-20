create database mis;
grant select, insert, delete on mis.* to 'mis'@'localhost' identified by 'password';
flush privileges;
use mis
create table if not exists files (
	id int not null auto_increment,
	sha512 char(129) not null,
	path varchar(255) not null,
	active boolean not null default True,
	node varchar(64) not null default '.',
	source varchar(255) null,
	primary key (id),
	fulltext index (path),
	index (node)
);
create table if not exists media ( name varchar(255) primary key, media_type varchar(16) );
create table if not exists media_files ( media varchar(255) references media.name, files varchar(255) references files.path );

create table if not exists containers (
	id int not null auto_increment, -- many containers may look the same
	container_type char(16) not null, -- what most people would call file type, probably
	media_type char(16) not null, -- audio, video, you know, 
	duration_usec mediumint not null, -- about two day's worth of milliseconds
	title varchar(255), -- important value usually in a container
	artist varchar(255),
	album varchar(255),
	year int, -- year of creation of media (as defined in the container)
	genre varchar(255),
	source varchar(255),
	comment varchar(255), -- also very common field
	primary key (id),
	fulltext index (title),
	index (year),
	index (media_type),
	index (duration_usec)
);

create table if not exists video_streams (
	id int not null auto_increment,
	codec char(4) not null,
	width smallint not null,
	height smallint not null,
	framerate float not null,
	duration_usec mediumint not null,
	bitrate mediumint null,
	primary key(id),
	index (duration_usec)
);

create table if not exists audio_streams (
	id int not null auto_increment,
	codec char(4) not null,
	channels tinyint not null,
	samplerate tinyint not null,
	bitrate mediumint not null,
	duration_usec mediumint not null,
	primary key (id),
	index (duration_usec)
);
