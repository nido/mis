create database mis;
grant select, insert, delete on mis.* to 'mis'@'localhost' identified by 'password';
flush privileges;
use mis

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
