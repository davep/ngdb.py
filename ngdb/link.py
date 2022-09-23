"""Provides a class that links some text to an offset in a guide."""

##############################################################################
# Python imports.
from typing import NamedTuple

##############################################################################
# A text/offset link within a guide.
class Link( NamedTuple ):
    """A link within a Norton Guide, comprising of some text and an offset."""

    #: The text of the link.
    text: str
    #: The offset of the link.
    offset: int

    def __str__( self ) -> str:
        """The text of the link."""
        return self.text

    def __int__( self ) -> int:
        """The offset of the link."""
        return self.offset

    @property
    def has_offset( self ) -> bool:
        """Does this link have an associated offset into the guide?

        :type: bool
        """
        return self.offset > 0

    def __bool__( self ) -> bool:
        """Does the link actually link anywhere?"""
        return self.has_offset

### link.py ends here
