# ChangeLog

## v0.7.0

**Released: 2025-03-01**

- Complete revamp of the repository.
  ([#4](https://github.com/davep/ngdb.py/pull/4))
  - Dropped support for `nginfo` -- I may revive it as part of a package of
    Norton Guide command line tools
  - Cleaned up a lot of documentation.
  - Added support for generating a proper set of hosted documentation.
  - Dropped support for Python 3.8.
  - Ensured that the code worked with Python 3.13.

## v0.6.1

**Released: 2024-04-02**

- Small bump to ensure that the `sdist` gets uploaded to PyPI too.

## v0.6.0

**Released: 2022-09-26**

- Sprinkled some Rich support, without a dependency on Rich, mostly as a way
  to try out a slight reworking of the parser classes, which should go on to
  benefit [ng2web](https://github.com/davep/ng2web).

## v0.5.0

**Released: 2022-09-19**

- Lots of internal tweaks
- Turned the prompt/offset tuples into `NamedTuple`s to make access to
  values read better in client code.

## v0.4.0

**Released: 2022-03-31**

- Added `make_dos_like`.

## v0.3.0

**Released: 2022-01-10**

- Added code to the Entry classes that allows proper access to previous and
  next entries.

## v0.2.0

**Released: 2022-01-07**

- Export `Entry` from the library.

## v0.1.0

**Released: 2021-10-30**

- Another alpha release, nothing really significant has changed, just
  tidying a few things up. Mostly marking this as another release as there's
  a tool I want to start building based on this, which will help test where
  I'm going with this. Having this released and on PyPI will help with that.

## v0.0.1

**Released: 2021-10-23**

- Initial release.

[//]: # (ChangeLog.md ends here)
