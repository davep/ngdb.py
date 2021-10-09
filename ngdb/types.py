"""Defines the IDs of the entry types that appear in a guide."""

##############################################################################
# Python imports.
from enum import Enum

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
