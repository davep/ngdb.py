"""Defines helpful types and values for the library.."""

##############################################################################
# Python imports.
from enum import Enum

##############################################################################
# Base exception.
class NGDBError( Exception ):
    """Base exception of all exceptions in the library."""

##############################################################################
# Unknown entry type error.
class UnknownEntryType( NGDBError ):
    """Type of an exception when faced with an unknown entry type."""

##############################################################################
# EOF error.
class NGEOF( NGDBError ):
    """Type of an exception thrown when doing things at or past EOF."""

##############################################################################
# Enum of Norton Guide database entry type IDs.
class EntryType( Enum ):
    """Types of entry in a guide."""

    SHORT = 0
    LONG  = 1
    MENU  = 2

    @classmethod
    def is_short( cls, test: int ) -> bool:
        """Is the value the ID of a short entry?

        :param int test: The value to test.
        :returns: ``True`` if it is a short, ``False`` if not.
        :rtype: bool
        """
        return cls( test ) is cls.SHORT

    @classmethod
    def is_long( cls, test: int ) -> bool:
        """Is the value the ID of a long entry?

        :param int test: The value to test.
        :returns: ``True`` if it is a long, ``False`` if not.
        :rtype: bool
        """
        return cls( test ) is cls.LONG

    @classmethod
    def is_menu( cls, test: int ) -> bool:
        """Is the value the ID of a menu?

        :param int test: The value to test.
        :returns: ``True`` if it is a menu, ``False`` if not.
        :rtype: bool
        """
        return cls( test ) is cls.MENU

### types.py ends here
