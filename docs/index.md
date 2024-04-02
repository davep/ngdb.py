# Introduction

Back in the mists of time, in the days of MS-DOS and Clipper programming,
[Norton Guide database files](https://en.wikipedia.org/wiki/Norton_Guides)
were a very popular form of hypertext help. Lots of information is still
kicking around inside such files. Over the years I've developed [a
reasonably long line of tools to help keep that information
available](http://www.davep.org/norton-guides/). Recently I realised that
I'd never written anything to access NG files from Python.

This library seeks to address that.

The reason for a library, as opposed to another converter or reader, is that
I actually do want to (and as of the time of writing have started to)
develop a new family of tools, that are nicely cross-platform, and will
serve the command line, the CHUI, the GUI and web interfaces. To make this
happen it makes sense that a solid core library for Norton Guide database
access is developed.

This is that library.

[//]: # (introduction.md ends here)