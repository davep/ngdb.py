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
$ pip install ngdb
```

## Using

See [the main documentation](https://blog.davep.org/ngdb.py/) for details on
using the library.

## Hacking

If you want to hack on the code yourself you'll find most of the routine
stuff you'd do when testing and the like in the `Makefile`. Type:

```sh
$ make
```

to get a list of available targets.

[//]: # (README.md ends here)
