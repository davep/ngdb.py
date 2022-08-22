# ngdb - A Python library for reading Norton Guide database files

[![PyPI version](https://badge.fury.io/py/ngdb.svg)](https://badge.fury.io/py/ngdb)

## Introduction

Back in the mists of time, in the days of MS-DOS and Clipper programming,
[Norton Guide database files](https://en.wikipedia.org/wiki/Norton_Guides)
were a very popular form of hypertext help. Lots of information is still
kicking around inside such files.

This library is another in [a reasonably long line of tools I've written to
help keep that information available](http://www.davep.org/norton-guides/).

## Installing

`ngdb` is [available from pypi](https://pypi.org/project/ngdb/) and can be
installed with `pip` or similar Python package tools:

```shell
$ pip3 install -U ngdb
```

## Tools

`ngdb` also installs the following tools:

- `nginfo`  
Simple tool that serves as an example of using the library: given a series
of files on the command line, it prints a simple list of the files showing
what type of NG file it is (Norton Guide or Expert Help), as well as its
title.

## Hacking

If you want to hack on the code yourself you'll find most of the routine
stuff you'd do when testing and the like in the `Makefile`. Type:

```sh
$ make help
```

to get a list of available targets.

## Using

The library is designed to provide a method of opening and reading Norton
Guide database files. The code here provides no methods for rendering the
content; there is no converter, no reader, etc. The library is designed to
be the core of such tools. One such tool, which as of the time of writing is
a work in progress, is [`ng2web`](https://github.com/davep/ng2web) -- a
template-driven tool that converts Norton Guide databases into HTML.

The main class in this library is `NortonGuide`. When called, with the path
to a Norton Guide file, it will open up the guide, load up all the key
information, and provide an interface for loading up the short and long
entries, loading up the menus, providing access to see-also items, etc.

At this point it probably goes without saying that this library is likely
only really useful to anyone who knows what a Norton Guide is and cares
about the content. As such, at least for the moment, this README will (with
apologies) assume some knowledge of what a Norton Guide is and its main
structure.

### Opening a guide

As mentioned above, a guide can be opened using the `NortonGuide` class. For
example:

```python
>>> from ngdb import NortonGuide
>>> guide = NortonGuide( "tests/guides/oslib.ng" )
```

Having loaded the guide you have access to the key information about it:

```python
>>> guide.title
'OSLIB v1.06'
>>> guide.credits
('³ OSLIB v1.06', '³ OSLIB Is Free Software with NO WARRANTY!', '³', '³ This library was compiled by Dave Pearson.', '³ davep@hagbard.demon.co.uk')
>>> guide.made_with
'Norton Guide'
>>> guide.menu_count
1
>>> guide.menus
(<Menu: OSLIB>,)
>>> guide.menus[ 0 ]
<Menu: OSLIB>
>>> guide.menus[ 0 ].title
'OSLIB'
>>> guide.menus[ 0 ].prompts
('Functions', 'FAQs', 'Revision History', 'Credits', 'About')
```

And so on. See the documentation produced by `make rtfm` for all the details
(eventually I aim to find a good way of generating and hosting full
documentation).

### Navigating a guide

Three methods exist for navigating a guide: `goto_first`, `goto` and `skip`.
As you may imagine, `goto_first` goes to the first entry in a guide, `goto`
goes to an entry at a specific byte offset in the guide, and `skip` skips
the current entry.

It should be noted here that an open guide has the content of a location
pointer. As you do things with the guide, the location will change.

When skipping, if you try and skip off the end of the file, a
`ngdb.types.NGEOF` will be thrown.

### Loading an entry

Load the current entry with the `load` method. Note that using this method
*doesn't* move the location pointer. When loading an entry you'll either get
a `Short` or a `Long` entry back. For example:

```python
>>> entry = guide.load()
>>> entry
<Short>
>>> entry.lines[ 0 ]
' OL_95AppTitle()          Set/get the Windows 95 application title.'
```

Plenty of properties that you'd expect exist. For now please take a look at
`make rtfm` for all the details (again, more comprehensive documentation
will be written).

### A simple example

To illustrate a simple use of the library, here's tiny bit of example code
that loads a guide, walks through all the entries, and prints the first line
from each one:

```python
from ngdb import NortonGuide

guide = NortonGuide( "tests/guides/oslib.ng" )

while not guide.eof:
    print( guide.load().lines[ 0 ] )
    guide.skip()
```

## Taking it from here

As mentioned above, there's a lot more to the library and the documentation
absolutely needs expanding. For now a `make rtfm` within the repository will
make the core documentation available. What needs to be added is a proper
tutorial on how to use the library to build a useful too.

This will follow.

Meanwhile, do also keep an eye on
[`ng2web`](https://github.com/davep/ng2web) as an example use. It is the
"proper" test of this library.

[//]: # (README.md ends here)
