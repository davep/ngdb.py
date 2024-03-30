"""Norton guide entry loading and holding code."""

##############################################################################
# Python compatibility hackage.
from __future__ import annotations

##############################################################################
# Python imports.
from typing import Callable, Final, Iterator, Type

##############################################################################
# Local imports.
from .link import Link
from .parser import RichText
from .reader import GuideReader
from .seealso import SeeAlso
from .types import EntryType, UnknownEntryType


##############################################################################
class EntryParent:
    """Class to load and hold the parent information for an entry."""

    def __init__(self, guide: GuideReader) -> None:
        """Constructor.

        Args:
            guide (GuideReader): The reader object for the guide.
        """
        self._line = guide.read_word()
        self._offset = guide.read_offset()
        self._menu = guide.read_word()
        self._prompt = guide.read_word()

    @property
    def offset(self) -> int:
        """int: The offset of the parent entry, if there is one."""
        return self._offset

    def __bool__(self) -> bool:
        """Is there a parent entry?

        Returns:
            bool: ``True`` if there is, ``False` if not.
        """
        return self.offset > 0

    @staticmethod
    def _non_test(value: int) -> int:
        """Ensure a -1 is a -1.

        Args:
            value (int): The value to clean up.

        Returns:
            int: The value with an intended -1 guaranteed.
        """
        return -1 if value == 0xFFFF else value

    @property
    def line(self) -> int:
        """int: The line in the parent entry that point to this entry.

        If there is no parent line this will be ``-1``. But also see
        ``has_line`` for a test for a parent entry line.
        """
        return self._non_test(self._line)

    @property
    def has_line(self) -> int:
        """bool: Does this entry have a parent entry line that points to it?"""
        return self.line != -1

    @property
    def menu(self) -> int:
        """int: The menu that relates to this entry.

        If there is no menu, this will be ``-1``. But also see ``has_menu``
        to test if there is a related menu.
        """
        return self._non_test(self._menu)

    @property
    def has_menu(self) -> bool:
        """bool: Is there a menu related to this entry?"""
        return self.menu != -1

    @property
    def prompt(self) -> int:
        """int: The menu prompt related to this entry.

        If there is no menu prompt, this will be ``-1``. But also see
        ``has_prompt`` to test if there is a related menu prompt.
        """
        return self._non_test(self._prompt)

    @property
    def has_prompt(self) -> bool:
        """bool: Is there a menu prompt related to this entry?"""
        return self.has_menu and self.prompt != -1


##############################################################################
TEntry = Type["Entry"]
"""Type of the type of an entry."""

##############################################################################
MAX_LINE_LENGTH: Final = 1024
"""int: Maximum size of a line we'll look for in a guide."""


##############################################################################
class Entry:
    """Norton Guide database entry class."""

    _map: dict[EntryType, TEntry] = {}
    """dict[EntryType,TEntry]: Holds the entry type mapper."""

    @classmethod
    def loads(cls, entry_type: EntryType) -> Callable[[TEntry], TEntry]:
        """Decorator for defining which class handles which entry type.

        Args:
            entry_type (EntryType): The ID of the entry type being handled.

        Returns:
            Callable[[TEntry],TEntry]: The decorator wrapper.
        """

        def _register(handler: TEntry) -> TEntry:
            """Inner decorator function."""
            cls._map[entry_type] = handler
            return handler

        return _register

    @classmethod
    def load(cls, guide: GuideReader) -> "Entry":
        """Load the entry at the current position in the guide.

        Args:
            guide (GuideReader): The reader object for the guide.

        Returns:
            Entry: The correct type of entry object.

        Raises:
            UnknownEntryType: Indicates that the entry type is unknown.
        """
        try:
            return cls._map[EntryType(guide.peek_word())](guide)
        except (ValueError, KeyError) as error:
            raise UnknownEntryType(
                f"Unknown guide entry type: {guide.peek_word()}"
            ) from error

    def __init__(self, guide: GuideReader) -> None:
        """Constructor.

        Args:
            guide (GuideReader): The reader object for the guide.
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
            guide (GuideReader): The reader object for the guide.
        """
        self._lines = tuple(
            guide.unrle(guide.read_strz(MAX_LINE_LENGTH)) for _ in range(len(self))
        )

    @property
    def offset(self) -> int:
        """int: The file offset of this entry."""
        return self._offset

    @property
    def type_id(self) -> int:
        """int: The numeric ID of the type of entry."""
        return self._type

    @property
    def size(self) -> int:
        """int: The size of the entry in bytes."""
        return self._size

    def __len__(self) -> int:
        """The number of lines in the entry.

        Returns:
            int: The number of lines.
        """
        return self._line_count

    @property
    def has_see_also(self) -> bool:
        """bool: Does this entry have any see-also items?"""
        return self._has_see_also > 0

    @property
    def parent(self) -> EntryParent:
        """EntryParent: Returns the parent entry information."""
        return self._parent

    @property
    def previous(self) -> int:
        """int: The location of the previous entry."""
        return self._previous

    @property
    def has_previous(self) -> bool:
        """bool: Is there a previous entry?"""
        return self.previous > 0

    @property
    def next(self) -> int:
        """int: The location of the next entry."""
        return self._next

    @property
    def has_next(self) -> bool:
        """bool: Is there a previous entry?"""
        return self.next > 0

    @property
    def lines(self) -> tuple[str, ...]:
        """tuple[str,...]: The lines of text in the entry."""
        return self._lines

    def __str__(self) -> str:
        """Return the text of the entry as a single string.

        Returns:
            str: The entry's text.
        """
        return "\n".join(self.lines)

    def __repr__(self) -> str:
        """Simply say the type of entry as the representation of the object.

        Returns:
            str: The name of the type of entry.
        """
        return f"<{self.__class__.__name__}: {self.offset}>"

    def __rich__(self) -> str:
        """Support being printed in a Rich-enhanced REPL.

        Note:
            See https://rich.readthedocs.io/en/stable/protocol.html

        Returns:
            str: Rich-friendly test.
        """
        return "\n".join(str(RichText(line)) for line in self.lines)


##############################################################################
@Entry.loads(EntryType.SHORT)
class Short(Entry):
    """Short Norton Guide database entry."""

    def __init__(self, guide: GuideReader) -> None:
        """Constructor.

        Args:
            guide (GuideReader): The reader object for the guide.
        """

        # Call the super class.
        super().__init__(guide)

        # Next up, load up all of the offsets associated with each of the
        # lines in the entry.
        self._offsets = tuple(self._load_offsets(guide))

        # Finally, load in the actual text.
        self._load_lines(guide)

    def _load_offsets(self, guide: GuideReader) -> Iterator[int]:
        """Load up the offsets for each of the lines in the entry.

        Args:
            guide (GuideReader): The reader object for the guide.

        Yields:
            int: The offset for each line in the entry.
        """
        for _ in range(len(self)):
            # Skip a word -- I don't know what this is.
            guide.skip(2)
            # Read the offset of the line.
            yield guide.read_offset()

    @property
    def offsets(self) -> tuple[int, ...]:
        """tuple[int,...]: The offsets for each of the lines in the entry."""
        return self._offsets

    def __getitem__(self, line: int) -> Link:
        """Get a line and its offset."""
        return Link(self.lines[line], self.offsets[line])

    def __iter__(self) -> Iterator[Link]:
        """The lines in the entry along with the offsets into the guide."""
        return (Link(*line) for line in zip(self.lines, self.offsets))


##############################################################################
@Entry.loads(EntryType.LONG)
class Long(Entry):
    """Long Norton Guide database entry."""

    def __init__(self, guide: GuideReader) -> None:
        """Constructor.

        Args:
            guide (GuideReader): The reader object for the guide.
        """

        # Call the super class.
        super().__init__(guide)

        # Load in the actual text.
        self._load_lines(guide)

        # Load up the see-also information.
        self._see_also = SeeAlso(guide, self.has_see_also)

    @property
    def see_also(self) -> SeeAlso:
        """SeeAlso: The see-also information for this entry."""
        return self._see_also

    def __getitem__(self, line: int) -> str:
        """Get a line from the entry."""
        return self.lines[line]

    def __iter__(self) -> Iterator[str]:
        """The lines in the entry."""
        return iter(self.lines)


### entry.py ends here
