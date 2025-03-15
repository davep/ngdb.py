# ngdb - A Python library for reading Norton Guide database files

[![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/davep/ngdb.py/style-lint-and-test.yaml)](https://github.com/davep/ngdb.py/actions)
[![GitHub commits since latest release](https://img.shields.io/github/commits-since/davep/ngdb.py/latest)](https://github.com/davep/ngdb.py/commits/main/)
[![GitHub Issues or Pull Requests](https://img.shields.io/github/issues/davep/ngdb.py)](https://github.com/davep/ngdb.py/issues)
[![GitHub Release Date](https://img.shields.io/github/release-date/davep/ngdb.py)](https://github.com/davep/ngdb.py/releases)
[![PyPI - License](https://img.shields.io/pypi/l/ngdb)](https://github.com/davep/ngdb.py/blob/main/LICENSE)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/ngdb)](https://github.com/davep/ngdb.py/blob/main/pyproject.toml)
[![PyPI - Version](https://img.shields.io/pypi/v/ngdb)](https://pypi.org/project/ngdb/)

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
