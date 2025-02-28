# Using ngdb

## Introduction

The library is designed to provide a method of opening and reading Norton
Guide database files. The code here provides no methods for rendering the
content; there is no converter, no reader application, etc; the library is
designed to be the core of such tools.

!!! information

    One such tool, which as of the time of writing is a work in progress, is
    [`ng2web`](https://github.com/davep/ng2web) -- a template-driven tool that
    converts Norton Guide databases into HTML.

The main class is [`NortonGuide`][ngdb.NortonGuide]. When called, with the
path to a Norton Guide file, it will open up the guide, load up all the key
information, and provide an interface for loading up the [short][ngdb.Short]
and [long][ngdb.Long] entries, loading up the [menus][ngdb.Menu], providing
access to [see-also items][ngdb.SeeAlso], etc.

At this point it probably goes without saying that `ngdb` is likely only
really useful to anyone who knows what a [Norton
Guide](https://en.wikipedia.org/wiki/Norton_Guides) is and cares about the
content. As such, at least for the moment, this documentation will (with
apologies) assume some knowledge of what a Norton Guide is and [its main
structure](https://www.davep.org/norton-guides/file-format/).

## Opening a guide

As mentioned above, a guide can be opened using the
[`NortonGuide`][ngdb.NortonGuide] class. For example:

```python
>>> from ngdb import NortonGuide
>>> guide = NortonGuide("tests/guides/oslib.ng")
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
>>> guide.menus[0]
<Menu: OSLIB>
>>> guide.menus[0].title
'OSLIB'
>>> guide.menus[0].prompts
('Functions', 'FAQs', 'Revision History', 'Credits', 'About')
```

The `NortonGuide` class can also be used with Python's `with` statement,
making it easy to quickly open a file and work with it. Here's an example of
a small tool that will open a guide and prints its title:

```python
--8<-- "docs/examples/open_guide.py"
```

## Navigating a guide

Three methods exist for navigating a guide:
[`goto_first`][ngdb.NortonGuide.goto_first], [`goto`][ngdb.NortonGuide.goto]
and [`skip`][ngdb.NortonGuide.skip]. As you may imagine, `goto_first` goes
to the first entry in a guide, `goto` goes to an entry at a specific byte
offset in the guide, and `skip` skips the current entry.

!!! tip

    It should be noted here that an open guide has the concept of a location
    pointer. As you do things with the guide, the location will change.

When skipping through a Norton Guide, if you try and skip off the end of the
file, an [`NGEOF`][ngdb.NGEOF] exception will be thrown.

Here's a simple example of all of this in action:

```python
--8<-- "docs/examples/navigate_guide.py"
```

While that example is fine for illustrating the [`NGEOF`][ngdb.NGEOF]
exception, really it would make more sense to use the
[`eof`][ngdb.NortonGuide.eof] property:

```python
--8<-- "docs/examples/navigate_guide_better.py"
```

## Reading entries

The most important content of a Norton Guide is its [entries][ngdb.Entry].
These come in two varieties, [short entries][ngdb.Short] and [long
entries][ngdb.Long]. An entry is loaded using
[`load`][ngdb.NortonGuide.load] and the correct type of entry will be
returned.

Here is an example of walking through a guide and printing out the types of
entries found:

```python
--8<-- "docs/examples/entry_types.py"
```

## Next steps

There's a lot more here that needs documenting, and over time I aim to
expand this guide. For now though, if you are familiar with Norton Guide
files and what they contain, the above should be enough to get you going
with the library.

The next step would be to read the lower-level API documentation for the
code, especially looking at the full documentation for the following:

- [`NortonGuide`][ngdb.NortonGuide]: for navigating the guide itself.
- [`Entry`][ngdb.Entry]: for common entry properties and methods.
- [`Short`][ngdb.Short]: for short entry properties and methods.
- [`Long`][ngdb.Long]: for long entry properties and methods.
- [`BaseParser`][ngdb.BaseParser]: for the base class for entry content
  parsers; this is what you'll inherit from if you want to write your own
  parser/converter to go from a guide's content to some other format.
- [`PlainText`][ngdb.PlainText]: an example parser that converts an entry's
  text into plain text.
- [`MarkupText`][ngdb.MarkupText]: an example parser that acts as the base
  class for parsers/converters that are markup-based; this would be a good
  place to inherit from if you want to make [a Norton Guide to HTML
  converter](https://github.com/davep/ng2web).
- [`RichText`][ngdb.parser.RichText]: an example implementation of
  [`MarkupText`][ngdb.MarkupText] that converts the content of an entry to
  [Rich's markup](https://rich.readthedocs.io/en/stable/protocol.html).

[//]: # (guide.md ends here)
