* weaves

** Packaging module is blkswn

The __init__.py script brings the module imports together.

There is a singleton Configuration.instance() with utility methods in
_Fetcher

_Queue.py _version.py _Stack.py are from this package's template. They can
be ignored.

__main__.py is a sample command-line script: not implemented.

** ETL Website scraper

This is a test system for an online website at

   https://www.anapioficeandfire.com/api/{type0}?page={page}&pageSize={pageSize}

It's only a test system and captures to text file.

*** Extract

 _Fetcher _IceFire and the test scripts test_Test and test_Test1

Load the data from the website in pages.
The test scripts write to text files.

*** Transform

_IceFireR provides an iterator for each record on the website pages, see test_Test2

There's a configuration file that I use to make use of a local web proxy.
blkswn.cfg see Fetcher. There are limits on the number of web-accesses.

The test scripts produce text files, in which the records are transformed
to dictionaries and each text file books.txt characters.txt or houses.txt 

** Load and Simple Analysis

You can then load the textfile output with a typing string "books" (or
{type0}, see IceFire's class variables.)

And do some simple analysis. 

This is tested and demonstrated in test_Test3

This stage uses a file but should be implemented as a iterator stream.

** Improvements

*** web-source: Link response header: next, first, prev, last

I didn't make full use of these. I just count the pages. Some databases
might enforce prev and next and not allow incremental page access.

*** Streamed filtering

IceFireA should be able to use an IceFireR as an iterator data source. And
caching would be a useful extension for that.



* This file's Emacs file variables

[  Local Variables: ]
[  mode:text ]
[  mode:outline-minor ]
[  mode:auto-fill ]
[  fill-column: 75 ]
[  coding: iso-8859-1-unix ]
[  comment-column:50 ]
[  comment-start: "[  "  ]
[  comment-end:"]" ]
[  End: ]

