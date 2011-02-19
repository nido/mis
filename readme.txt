Media Information System

This is an attempt to make it feasable to handle media libraries
of ridiculous proportions. Because of that, it uses a library of
its own asynchronously from the accurate metadata in the file.

Rediculous proportions at time of writing means bigger then two
terabyte. more generally speaking: more then fits on a single unit
of (consumer) storage, more then can be read completely (by the computer) in
24 hours, and more entries then can be cached by the processor.

This means it should synchronise from time to time and the media
library itself should be reasonably static. Should the data get too much
out of sync, mis becomes worthless; so be sure to activate the
synchronisation when any is created.

the files are also decoupled from the actual media. This is handy
should one have three copies of a single media. support for
divided (e.g. film_part1.mpg and film_part2.mpg) may be included
in the future.

there is an 'active' boolean in the files list. this should be
deactivated rather then the entry removed once the file is
unavailable or replaced with another copy (given the sha1 hash).
development is underway to allow redundancy of files or media
over different sites.

general list of todo stuff

clean up extensions business (a.k.a. grab superiour list).
collections (of one episode, series, series of series, universes)
media/file/filetype/media-specifics recogniser.
`watched' list
double file checker
connect to external instance
up/download files
talk to the admin (missing/double files, other problems)
redundant jbod storage usage/detection
storage importance settings (unimportant - no redundancy,
	superimportant - omnipresent redundancy)
user interface
configuration of options
