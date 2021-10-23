# ngdb - A Python library for reading Norton Guide database files

## Introduction

Back in the mists of time, in the days of MS-DOS and Clipper programming,
[Norton Guide database files](https://en.wikipedia.org/wiki/Norton_Guides)
were a very popular form of hypertext help. Lots of information is still
kicking around inside such files.

This library is another in [a reasonably long line of tools I've written to
help keep that information available](http://www.davep.org/norton-guides/).

## TODO

The library is now at a point where the reading of guides works fine, and it
has plenty of test coverage too (in fact it should be 100% if I've not
messed up). What's lacking right now us user documentation and an example
tool or two.

They are to come.

My intention is to make a binary utility or two that go along with this
library that will do things like turn a Norton Guide database into a series
of HTML pages, or extract as a Markdown document, or something like that.

Eventually I'll create another project or two off the back of this, which
will be separate from this. For example, I'd like to create a CHUI reader
all in Python, and also perhaps a guide server based on Flask.

For now though... if you're happy diving through the library docs (`make
rtfm` is your friend), there should be enough to get started.

[//]: # (README.md ends here)
