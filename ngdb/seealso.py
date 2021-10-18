"""See-also loading/holding code."""

##############################################################################
# Python imports.
from typing import Tuple, Iterator

##############################################################################
# Local imports.
from .reader import GuideReader
from .menu   import Menu

##############################################################################
# Class that loads and holds a see-also collection.
class SeeAlso:
    """Class to load and hold all the see alsos for a long entry."""

    #: Max number of see also items we'll handle.
    #
    # This is the limit published in the Expert Help Compiler manual and,
    # while this limit isn't really needed in this code, it does help guard
    # against corrupt guides.
    MAX_SEE_ALSO = 20

    def __init__( self, guide: GuideReader, load: bool ) -> None:
        """Constructor.

        :param GuideReader guide: The reader object for the guide.
        :param bool load: Should we bother trying to load any?

        The ``load`` parameter might look a bit daft, and it is, but a
        Norton Guide has a flag to say if there are any see-also entries
        *and* a count value later on, which won't be there and won't be 0 if
        the flag is 0. So... we pass the flag in here and just have a
        see-also collection that has nothing in it.

        I could, of course, make the use of this class optional but that
        feels icky.
        """

        # Should we actually bother trying to load anything?
        if load:

            # Get the count of see-also entries.
            self._count = min( guide.read_word(), self.MAX_SEE_ALSO )

            # Get the offsets for each of the see-also entries.
            self._offsets = tuple( guide.read_long() for _ in range( len( self ) ) )

            # Get the prompts for each of the see-also items.
            self._prompts = tuple(
                guide.unrle( guide.read_strz( Menu.MAX_PROMPT_LENGTH ) )
                for _ in range( len( self ) )
            )

        else:
            # Nope, don't load, just zero everything out.
            self._count   = 0
            self._offsets = ()
            self._prompts = ()

    def __len__( self ) -> int:
        """Get the count of see-also entries."""
        return self._count

    @property
    def offsets( self ) -> Tuple[ int, ... ]:
        """The file offset that each see-also points to.

        :type: Tuple[int,...]
        """
        return self._offsets

    @property
    def prompts( self ) -> Tuple[ str, ... ]:
        """The prompt for each see-also.

        :type: Tuple[str,...]
        """
        return self._prompts

    def __getitem__( self, see_also: int ) -> Tuple[ str, int ]:
        """Get a see-also's information."""
        return self.prompts[ see_also ], self.offsets[ see_also ]

    def __iter__( self ) -> Iterator[ Tuple[ str, int ] ]:
        """Get an iterator of see-also prompt and offset pairs."""
        return zip( self.prompts, self.offsets )

### seealso.py ends here
