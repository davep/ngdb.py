"""Defines helpful types and values for the library.."""

##############################################################################
# Python imports.
from enum import Enum


##############################################################################
class NGDBError(Exception):
    """Base exception of all exceptions in the library."""


##############################################################################
class NGEOF(NGDBError):
    """Type of an exception thrown when doing things at or past EOF."""


##############################################################################
class UnknownEntryType(NGEOF):
    """Type of an exception when faced with an unknown entry type.

    Note:
        This class is a subclass of [`NGEOF`][ngdb.NGEOF] so if you are
        writing code that walks a guide and you want to stop once an unknown
        guide type is found (often indicating a corrupted guide), you can
        safely catch [`NGEOF`][ngdb.NGEOF] and this exception will be
        handled.
    """


##############################################################################
class EntryType(Enum):
    """Types of entry in a guide."""

    SHORT = 0
    """The record ID for a short entry in a Norton Guide database."""

    LONG = 1
    """The record ID for a long entry in a Norton Guide database."""

    MENU = 2
    """The record ID for a menu in a Norton Guide database."""

    @classmethod
    def is_short(cls, test: int) -> bool:
        """Is the value the ID of a short entry?

        Args:
            test: The value to test.

        Returns:
            [`True`][True] if it is a short, [`False`][False] if not.
        """
        return cls(test) is cls.SHORT

    @classmethod
    def is_long(cls, test: int) -> bool:
        """Is the value the ID of a long entry?

        Args:
            test: The value to test.

        Returns:
            [`True`][True] if it is a long, [`False`][False] if not.
        """
        return cls(test) is cls.LONG

    @classmethod
    def is_menu(cls, test: int) -> bool:
        """Is the value the ID of a menu?

        Args:
            test: The value to test.

        Returns:
            [`True`][True] if it is a menu, [`False`][False] if not.
        """
        return cls(test) is cls.MENU


### types.py ends here
