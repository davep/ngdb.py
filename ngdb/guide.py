"""Defines the class for opening and managing a Norton Guide database."""

##############################################################################
# Python imports.
from pathlib import Path
from typing  import Tuple, Iterator, Union

##############################################################################
# Local imports.
from .types  import EntryType
from .reader import GuideReader
from .menu   import Menu
from .entry  import Entry

##############################################################################
# Main Norton Guide class.
class NortonGuide:
    """Norton Guide database wrapper class.

    :ivar ~pathlib.Path path: The path of the database.
    """

    #: Lookup for valid database magic markers.
    MAGIC = {
        "EH": "Expert Help",
        "NG": "Norton Guide"
    }

    #: The length of a title in the header.
    TITLE_LENGTH = 40

    #: The length of a line in the credits.
    CREDIT_LENGTH = 66

    def __init__( self, guide: Union[ str, Path ] ) -> None:
        """Constructor.

        :param Union[str,~pathlib.Path] guide: The guide to open.
        """

        # Remember the guide path.
        self.path = Path( guide )

        # Attempt to open the guide. Note that we're going to hold it open
        # until we're asked to close it in the close method, so we also
        # nicely ask pylint to hush.
        self._guide = GuideReader( self.path )

        # Now, having opened it fine, read in the header.
        self._read_header()

        # Having read in the header, does it look like it's a Norton Guide
        # database we've been pointed at?
        if self.is_a:
            # Seems so. In that case sort the menus.
            self._menus = tuple( menu for menu in self._read_menus() )

            # The number of menus should be correct at this point.
            assert len( self._menus ) == self._menu_count

            # At this point we should be sat on top of the first entry, so
            # let's remember where that is.
            self._first_entry = self._guide.pos

    def _read_header( self ) -> None:
        """Read the header of the Norton Guide database."""

        # First two bytes are the magic.
        self._magic = self._guide.read_str( 2, False )

        # Skip 4 bytes; to this day I'm not sure what they're for.
        self._guide.skip( 4 )

        # Read the count of menu options.
        self._menu_count = self._guide.read_word( False )

        # Read the title of the guide.
        self._title = self._guide.read_str( self.TITLE_LENGTH, False )

        # Read the credits for the guide.
        self._credits = tuple(
            self._guide.read_str( self.CREDIT_LENGTH, False ) for _ in range( 5 )
        )

    def _read_menus( self ) -> Iterator[ Menu ]:
        """Read the menus from the guide.

        :yields: Menu
        """
        while EntryType.is_menu( self._guide.peek_word() ):
            yield Menu( self._guide )

    @property
    def is_open( self ) -> bool:
        """Is the guide open?

        :type: bool
        """
        # Note that I first ensure that this instance actually does have a
        # `_guide` property as it's possible that an exception gets thrown
        # in the constructor and I have a __del__ method to ensure that the
        # handle is closed if it's open (see below). This means that it's
        # possible to fail to be fully constructed yet also asked to be
        # destructed.
        return hasattr( self, "_guide" ) and not self._guide.closed

    @property
    def is_a( self ) -> bool:
        """Is the guide actually a Norton Guide database?

        :type: bool
        """
        return self._magic in self.MAGIC

    def close( self ) -> None:
        """Close the guide, if it's open.

        **NOTE:** Closing the guide when it isn't open is a non-op. It's
        always safe to make this call.
        """
        if self.is_open:
            self._guide.close()

    def __del__( self ) -> None:
        """Ensure we close the handle to the guide if we're deleted."""
        self.close()

    @property
    def menu_count( self ) -> int:
        """The count of menu options in the guide.

        :type: int
        """
        return self._menu_count

    @property
    def title( self ) -> str:
        """The title of the guide.

        :type: str
        """
        return self._title

    @property
    def credits( self ) -> Tuple[ str, ... ]:
        """The credits for the guide.

        :type: Tuple[str,...]
        """
        return self._credits

    @property
    def menus( self ) -> Tuple[ Menu, ... ]:
        """The menus for the guide.

        :type: Tuple[Menu,...]
        """
        return self._menus

    def goto( self, pos: int ) -> "NortonGuide":
        """Go to a specific location in the guide.

        :param int pos: The position to go to.
        :returns: self
        :rtype: NortonGuide
        """
        self._guide.goto( pos )
        return self

    def goto_first( self ) -> "NortonGuide":
        """Go to the first entry in the guide.

        :returns: self
        :rtype: NortonGuide
        """
        return self.goto( self._first_entry )

    def skip( self ) -> "NortonGuide":
        """Skip the current entry.

        :returns: self
        :rtype: NortonGuide
        """
        self._guide.skip_entry()
        return self

    @property
    def eof( self ) -> bool:
        """Are we at the end of the guide?

        :type: bool
        """
        return self._guide.pos >= self.path.stat().st_size

    def load( self ) -> Entry:
        """Load the entry at the current position.

        :returns: The entry found at the current position.
        :rtype: Entry
        """
        return Entry.load( self._guide )

    def __repr__( self ) -> str:
        """The string representation of the guide."""
        return f"<{self.__class__.__name__}: {self.path.resolve()}>"

### guide.py ends here
