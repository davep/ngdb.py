"""Provides a class that links some text to an offset in a guide."""

##############################################################################
# Python imports.
from typing import NamedTuple


##############################################################################
class Link(NamedTuple):
    """A link within a Norton Guide, comprising of some text and an offset."""

    text: str
    """The text of the link."""

    offset: int
    """The offset of the link."""

    def __str__(self) -> str:
        """Returns the text of the link.

        Returns:
            The text for the link.
        """
        return self.text

    def __int__(self) -> int:
        """Returns the offset of the link.

        Returns:
            The offset for the link.
        """
        return self.offset

    @property
    def has_offset(self) -> bool:
        """Does this link have an associated offset into the guide?"""
        return self.offset > 0

    def __bool__(self) -> bool:
        """Does the link actually link anywhere?

        Returns:
            [`True`][True] if the link links somewhere, [`False`][False] if not.
        """
        return self.has_offset


### link.py ends here
