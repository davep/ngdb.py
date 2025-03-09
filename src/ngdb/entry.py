"""Norton guide entry loading and holding code."""

##############################################################################
# Python compatibility hackage.
from __future__ import annotations

##############################################################################
# Python imports.
from typing import Final, Iterator

##############################################################################
# Local imports.
from .link import Link
from .parser import RichText
from .reader import GuideReader
from .seealso import SeeAlso


##############################################################################
class EntryParent:
    """Class to load and hold the parent information for an entry."""

    def __init__(self, guide: GuideReader) -> None:
        """Constructor.

        Args:
            guide: The reader object for the guide.
        """
        self._line = guide.read_word()
        self._offset = guide.read_offset()
        self._menu = guide.read_word()
        self._prompt = guide.read_word()

    @property
    def offset(self) -> int:
        """The offset of the parent entry, if there is one."""
        return self._offset

    def __bool__(self) -> bool:
        """Is there a parent entry?

        Returns:
            [`True`][True] if there is, [`False`][False] if not.
        """
        return self.offset > 0

    @staticmethod
    def _non_test(value: int) -> int:
        """Ensure a -1 is a -1.

        Args:
            value: The value to clean up.

        Returns:
            The value with an intended -1 guaranteed.
        """
        return -1 if value == 0xFFFF else value

    @property
    def line(self) -> int:
        """The line in the parent entry that point to this entry.

        If there is no parent line this will be ``-1``. But also see
        [`has_line`][ngdb.entry.EntryParent.has_line] for a test for a
        parent entry line.
        """
        return self._non_test(self._line)

    @property
    def has_line(self) -> int:
        """Does this entry have a parent entry line that points to it?"""
        return self.line != -1

    @property
    def menu(self) -> int:
        """The menu that relates to this entry.

        If there is no menu, this will be `-1`. But also see
        [`has_menu`][ngdb.entry.EntryParent.has_menu] to test if there is a
        related menu.
        """
        return self._non_test(self._menu)

    @property
    def has_menu(self) -> bool:
        """Is there a menu related to this entry?"""
        return self.menu != -1

    @property
    def prompt(self) -> int:
        """The menu prompt related to this entry.

        If there is no menu prompt, this will be `-1`. But also see
        [`has_prompt`][ngdb.entry.EntryParent.has_prompt] to test if there
        is a related menu prompt.
        """
        return self._non_test(self._prompt)

    @property
    def has_prompt(self) -> bool:
        """Is there a menu prompt related to this entry?"""
        return self.has_menu and self.prompt != -1


##############################################################################
MAX_LINE_LENGTH: Final[int] = 1024
"""Maximum size of a line we'll look for in a guide."""


##############################################################################
class Entry:
    """Norton Guide database entry class."""

    def __init__(self, guide: GuideReader) -> None:
        """Constructor.

        Args:
            guide: The reader object for the guide.
        """

        # Load up the main details for the entry.
        self._offset = guide.pos
        self._type = guide.read_word()
        self._size = guide.read_word()
        self._line_count = guide.read_word()
        self._has_see_also = guide.read_word()
        self._parent = EntryParent(guide)
        self._previous = guide.read_offset()
        self._next = guide.read_offset()

        # Set up for loading in the lines.
        self._lines: tuple[str, ...] = ()

    def _load_lines(self, guide: GuideReader) -> None:
        """Load in all of the lines of text, from this point.

        Args:
            guide: The reader object for the guide.
        """
        self._lines = tuple(
            guide.unrle(guide.read_strz(MAX_LINE_LENGTH)) for _ in range(len(self))
        )

    @property
    def offset(self) -> int:
        """The file offset of this entry."""
        return self._offset

    @property
    def type_id(self) -> int:
        """The numeric ID of the type of entry."""
        return self._type

    @property
    def size(self) -> int:
        """The size of the entry in bytes."""
        return self._size

    def __len__(self) -> int:
        """The number of lines in the entry.

        Returns:
            The number of lines.
        """
        return self._line_count

    @property
    def has_see_also(self) -> bool:
        """Does this entry have any see-also items?"""
        return self._has_see_also > 0

    @property
    def parent(self) -> EntryParent:
        """Returns the parent entry information."""
        return self._parent

    @property
    def previous(self) -> int:
        """The location of the previous entry."""
        return self._previous

    @property
    def has_previous(self) -> bool:
        """Is there a previous entry?"""
        return self.previous > 0

    @property
    def next(self) -> int:
        """The location of the next entry."""
        return self._next

    @property
    def has_next(self) -> bool:
        """Is there a next entry?"""
        return self.next > 0

    @property
    def lines(self) -> tuple[str, ...]:
        """The lines of text in the entry."""
        return self._lines

    def __str__(self) -> str:
        """Return the text of the entry as a single string.

        Returns:
            The entry's text.
        """
        return "\n".join(self.lines)

    def __repr__(self) -> str:
        """Returns a string representation of the object.

        Returns:
            The name of the type of entry.
        """
        return f"<{self.__class__.__name__}: {self.offset}>"

    def __rich__(self) -> str:
        """Support being printed in a [Rich-enhanced REPL](https://rich.readthedocs.io/en/stable/protocol.html).

        Returns:
            Rich-friendly test.
        """
        return "\n".join(str(RichText(line)) for line in self.lines)


##############################################################################
class Short(Entry):
    """Short Norton Guide database entry."""

    def __init__(self, guide: GuideReader) -> None:
        """Constructor.

        Args:
            guide: The reader object for the guide.
        """
        super().__init__(guide)
        self._offsets = tuple(self._load_offsets(guide))
        """The offsets for each line in the short entry."""
        self._load_lines(guide)

    def _load_offsets(self, guide: GuideReader) -> Iterator[int]:
        """Load up the offsets for each of the lines in the entry.

        Args:
            guide: The reader object for the guide.

        Yields:
            The offset for each line in the entry.
        """
        for _ in range(len(self)):
            # Skip a word -- I don't know what this is.
            guide.skip(2)
            # Read the offset of the line.
            yield guide.read_offset()

    @property
    def offsets(self) -> tuple[int, ...]:
        """The offsets for each of the lines in the entry."""
        return self._offsets

    def __getitem__(self, line: int) -> Link:
        """Get a line and its offset.

        Args:
            line: The line to get the link information for.

        Returns:
            The link associated with that line.
        """
        return Link(self.lines[line], self.offsets[line])

    def __iter__(self) -> Iterator[Link]:
        """The lines in the entry along with the offsets into the guide.

        Returns:
            An iterator of link data.
        """
        return (Link(*line) for line in zip(self.lines, self.offsets))


##############################################################################
class Long(Entry):
    """Long Norton Guide database entry."""

    def __init__(self, guide: GuideReader) -> None:
        """Constructor.

        Args:
            guide: The reader object for the guide.
        """
        super().__init__(guide)
        self._load_lines(guide)
        self._see_also = SeeAlso(guide, self.has_see_also)
        """The see-also data for the long entry."""

    @property
    def see_also(self) -> SeeAlso:
        """The see-also information for this entry."""
        return self._see_also

    def __getitem__(self, line: int) -> str:
        """Get a line from the entry.

        Args:
            line: The lint to get.

        Returns:
            The line.
        """
        return self.lines[line]

    def __iter__(self) -> Iterator[str]:
        """The lines in the entry.

        Returns:
            An iterator of strings that are the lines in the entry.
        """
        return iter(self.lines)


### entry.py ends here
