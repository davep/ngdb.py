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

[//]: # (README.md ends here)
