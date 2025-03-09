"""Defines the class for opening and managing a Norton Guide database."""

##############################################################################
# Python compatibility hackage.
from __future__ import annotations

##############################################################################
# Python imports.
from functools import wraps
from pathlib import Path
from typing import Any, Callable, Final, Iterator, TypeVar

##############################################################################
# Typing backward compatibility.
from typing_extensions import Self

##############################################################################
# Local imports.
from .entry import Long, Short
from .menu import Menu
from .reader import GuideReader
from .types import NGEOF, EntryType, UnknownEntryType

##############################################################################
EOFResult = TypeVar("EOFResult")
"""Return type of a method decorated with [`@not_eof`][ngdb.guide.not_eof]."""


##############################################################################
def not_eof(meth: Callable[..., EOFResult]) -> Callable[..., EOFResult]:
    """Decorator to ensure a guide isn't at EOF before executing a method.

    Args:
        meth: The method fo protect.

    Returns:
        The guard.

    This decorator is used as part of [`NortonGuide`][ngdb.NortonGuide], to
    decorate functions that should test for being
    [`eof`][ngdb.NortonGuide.eof] before the work of the method is done. If
    the guide is `eof` [`NGEOF`][ngdb.types.NGEOF] will be raised.
    """

    @wraps(meth)
    def _guard(self: NortonGuide, *args: Any, **kwargs: Any) -> EOFResult:
        """Guard the given method call."""
        if self.eof:
            raise NGEOF
        return meth(self, *args, **kwargs)

    return _guard


##############################################################################
class NortonGuide:
    """Norton Guide database wrapper class."""

    MAGIC: Final[dict[str, str]] = {"EH": "Expert Help", "NG": "Norton Guide"}
    """Lookup for valid database magic markers."""

    TITLE_LENGTH: Final[int] = 40
    """The length of a title in the header."""

    CREDIT_LENGTH: Final[int] = 66
    """The length of a line in the credits."""

    def __init__(self, guide: str | Path) -> None:
        """Constructor.

        Args:
            guide: The guide to open.
        """

        self._path = Path(guide)
        """The path to the guide."""

        # Attempt to open the guide. Note that we're going to hold it open
        # until we're asked to close it in the close method, so we also
        # nicely ask pylint to hush.
        self._guide = GuideReader(self._path)

        # Now, having opened it fine, read in the header.
        self._read_header()

        # Having read in the header, does it look like it's a Norton Guide
        # database we've been pointed at?
        if self.is_a:
            # Seems so. In that case sort the menus.
            self._menus = tuple(menu for menu in self._read_menus())

            # The number of menus should be correct at this point.
            assert len(self._menus) == self._menu_count

            # At this point we should be sat on top of the first entry, so
            # let's remember where that is.
            self._first_entry = self._guide.pos

    @property
    def path(self) -> Path:
        """The path to the guide."""
        return self._path

    def _read_header(self) -> None:
        """Read the header of the Norton Guide database."""

        # First two bytes are the magic.
        self._magic = self._guide.read_str(2, False)

        # Skip 4 bytes; to this day I'm not sure what they're for.
        self._guide.skip(4)

        # Read the count of menu options.
        self._menu_count = self._guide.read_word(False)

        # Read the title of the guide.
        self._title = self._guide.read_str(self.TITLE_LENGTH, False)

        # Read the credits for the guide.
        self._credits = tuple(
            self._guide.read_str(self.CREDIT_LENGTH, False) for _ in range(5)
        )

    def _read_menus(self) -> Iterator[Menu]:
        """Read the menus from the guide.

        Yields
            A menu from the guide.
        """
        while EntryType.is_menu(self._guide.peek_word()):
            yield Menu(self._guide)

    @property
    def is_open(self) -> bool:
        """Is the guide open?"""
        # Note that I first ensure that this instance actually does have a
        # `_guide` property as it's possible that an exception gets thrown
        # in the constructor and I have a __del__ method to ensure that the
        # handle is closed if it's open (see below). This means that it's
        # possible to fail to be fully constructed yet also asked to be
        # destructed.
        return hasattr(self, "_guide") and not self._guide.closed

    @property
    def is_a(self) -> bool:
        """Is the guide actually a Norton Guide database?"""
        return self.magic in self.MAGIC

    def close(self) -> None:
        """Close the guide, if it's open.

        Note:
            Closing the guide when it isn't open is a non-op. It's always
            safe to make this call.
        """
        if self.is_open:
            self._guide.close()

    def __enter__(self) -> Self:
        """Handle entry to context."""
        return self

    def __exit__(self, *_: Any) -> None:
        """Handle exit from context."""
        self.close()

    def __del__(self) -> None:
        """Ensure we close the handle to the guide if we're deleted."""
        self.close()

    @property
    def menu_count(self) -> int:
        """The count of menu options in the guide."""
        return self._menu_count

    @property
    def title(self) -> str:
        """The title of the guide."""
        return self._title

    @property
    def credits(self) -> tuple[str, ...]:
        """The credits for the guide."""
        return self._credits

    @property
    def magic(self) -> str:
        """The magic value for the guide.

        This tells us if the file is likely a Norton Guide database or not.
        It's always a two-character string and, normally, is ''NG''.
        However, if the guide was made for Expert Help, it could be ''EH''.
        """
        return self._magic

    @property
    def made_with(self) -> str:
        """The name of the tool that was used to make the guide."""
        return self.MAGIC.get(self.magic, "Unknown")

    @property
    def menus(self) -> tuple[Menu, ...]:
        """The menus for the guide."""
        return self._menus

    def goto(self, pos: int) -> Self:
        """Go to a specific location in the guide.

        Args:
            pos: The position to go to.

        Returns:
            Returns ``self``.
        """
        self._guide.goto(pos)
        return self

    def goto_first(self) -> Self:
        """Go to the first entry in the guide.

        Returns:
            Returns ``self``.
        """
        return self.goto(self._first_entry)

    @not_eof
    def skip(self) -> Self:
        """Skip the current entry.

        Returns:
            Returns ``self``.

        Raises:
            NGEOF: If we attempt to skip when at EOF.
        """
        self._guide.skip_entry()
        return self

    @property
    def eof(self) -> bool:
        """Are we at the end of the guide?"""
        return self._guide.pos >= self._path.stat().st_size

    @not_eof
    def load(self) -> Short | Long:
        """Load the entry at the current position.

        Returns:
            The entry found at the current position. Either a
              [`Short`][ngdb.Short] or a [`Long`][ngdb.Long] entry.

        Raises:
            NGEOF: If we attempt to load when at EOF.
            UnknownEntryType: If the type wasn't an entry.
        """
        pos = self._guide.pos
        try:
            match EntryType(self._guide.peek_word()):
                case EntryType.SHORT:
                    return Short(self._guide)
                case EntryType.LONG:
                    return Long(self._guide)
                case EntryType.MENU:
                    raise UnknownEntryType(
                        "Expecting a short or long entry but got a menu"
                    )
        except ValueError:
            raise UnknownEntryType(
                f"Unknown entry type: {self._guide.peek_word()}"
            ) from None
        finally:
            self.goto(pos)

    def __iter__(self) -> Iterator[Short | Long]:
        """Allow iterating through every entry in the guide.

        Yields:
            An entry from the guide. Either a [`Short`][ngdb.Short] or a
              [`Long`][ngdb.Long] entry.

        Raises:
            UnknownEntryType: If an unknown type of entry is encountered.
        """
        # Here I try my best to do this in a way that no other operations
        # that consume this iterator will affect it. So, starting with the
        # first entry...
        entry = self.goto_first().load()
        while True:
            try:
                # ...pass up the current entry...
                yield entry
                # ...and then, assuming the worst (that our caller may have
                # moved around the guide while consuming that entry), we
                # pointedly go back to it, skip it and load whatever's next.
                entry = self.goto(entry.offset).skip().load()
            except NGEOF:
                # EOF was thrown so let's finish the iterator.
                break

    def __repr__(self) -> str:
        """The string representation of the guide.

        Returns:
            The guide's full path/file name.
        """
        return f'<{self.__class__.__name__}: "{self}">'

    def __str__(self) -> str:
        """The string representation of the guide.

        Returns:
            The guide's full path/file name.
        """
        return str(self._path.resolve())


### guide.py ends here
