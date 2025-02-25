"""Defines helpful types and values for the library.."""

##############################################################################
# Python imports.
from enum import Enum


##############################################################################
class NGDBError(Exception):
    """Base exception of all exceptions in the library."""


##############################################################################
class UnknownEntryType(NGDBError):
    """Type of an exception when faced with an unknown entry type."""


##############################################################################
class NGEOF(NGDBError):
    """Type of an exception thrown when doing things at or past EOF."""


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
            ``True`` if it is a short, ``False`` if not.
        """
        return cls(test) is cls.SHORT

    @classmethod
    def is_long(cls, test: int) -> bool:
        """Is the value the ID of a long entry?

        Args:
            test: The value to test.

        Returns:
            ``True`` if it is a long, ``False`` if not.
        """
        return cls(test) is cls.LONG

    @classmethod
    def is_menu(cls, test: int) -> bool:
        """Is the value the ID of a menu?

        Args:
            test: The value to test.

        Returns:
            ``True`` if it is a menu, ``False`` if not.
        """
        return cls(test) is cls.MENU


### types.py ends here
