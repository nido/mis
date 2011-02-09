create database mis;
use mis
create table if not exists files ( sha512 char(129) not null, path varchar(255) primary key, active boolean not null default True, node varchar(64) not null default '.' );
create table if not exists media ( name varchar(255) primary key, media_type varchar(16) );
create table if not exists media_files ( media varchar(255) references media.name, files varchar(255) references files.path );
grant select, insert, delete on mis.* to 'mis'@'localhost' identified by 'password';
flush privileges;
