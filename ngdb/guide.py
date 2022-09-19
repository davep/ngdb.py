"""Defines the class for opening and managing a Norton Guide database."""

##############################################################################
# Python imports.
from pathlib   import Path
from typing    import Tuple, Iterator, Union, Callable, Any, Final
from functools import wraps

##############################################################################
# Local imports.
from .types  import EntryType, NGEOF
from .reader import GuideReader
from .menu   import Menu
from .entry  import Entry

##############################################################################
# EOF-protection method decorator.
def not_eof( meth: Callable[ ..., Any ] ) -> Callable[ ..., Any ]:
    """Decorator to ensure a guide isn't at EOF before executing a method.

    :param Callable[...,Any] meth: The method fo protect.
    :returns: The guard.
    :rtype: Callable[...,Any]
    """
    @wraps( meth )
    def _guard( self: "NortonGuide", *args: Any, **kwargs: Any ) -> Any:
        """Guard the given method call."""
        if self.eof:
            raise NGEOF
        return meth( self, *args, **kwargs )
    return _guard

##############################################################################
# Main Norton Guide class.
class NortonGuide:
    """Norton Guide database wrapper class.

    :ivar ~pathlib.Path path: The path of the database.
    """

    #: Lookup for valid database magic markers.
    MAGIC: Final = {
        "EH": "Expert Help",
        "NG": "Norton Guide"
    }

    #: The length of a title in the header.
    TITLE_LENGTH: Final = 40

    #: The length of a line in the credits.
    CREDIT_LENGTH: Final = 66

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
        return self.magic in self.MAGIC

    def close( self ) -> None:
        """Close the guide, if it's open.

        **NOTE:** Closing the guide when it isn't open is a non-op. It's
        always safe to make this call.
        """
        if self.is_open:
            self._guide.close()

    def __enter__( self ) -> "NortonGuide":
        """Handle entry to context."""
        return self

    def __exit__( self, *_: Any ) -> None:
        """Handle exit from context."""
        self.close()

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
    def magic( self ) -> str:
        """The magic value for the guide.

        :type: str

        This tells us if the file is likely a Norton Guide database or not.
        It's always a two-character string and, normally, is ''NG''.
        However, if the guide was made for Expert Help, it could be ''EH''.
        """
        return self._magic

    @property
    def made_with( self ) -> str:
        """The name of the tool that was used to make the guide.

        :type: str
        """
        return self.MAGIC.get( self.magic, "Unknown" )

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

    @not_eof
    def skip( self ) -> "NortonGuide":
        """Skip the current entry.

        :returns: self
        :rtype: NortonGuide
        :raises NGEOF: If we attempt to skip when at EOF.
        """
        self._guide.skip_entry()
        return self

    @property
    def eof( self ) -> bool:
        """Are we at the end of the guide?

        :type: bool
        """
        return self._guide.pos >= self.path.stat().st_size

    @not_eof
    def load( self ) -> Entry:
        """Load the entry at the current position.

        :returns: The entry found at the current position.
        :rtype: Entry
        :raises NGEOF: If we attempt to load when at EOF.
        """
        pos = self._guide.pos
        try:
            return Entry.load( self._guide )
        finally:
            self.goto( pos )

    def __iter__( self ) -> Iterator[ Entry ]:
        """Allow iterating through every entry in the guide.

        :yields: Entry
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
                entry = self.goto( entry.offset ).skip().load()
            except NGEOF:
                # EOF was thrown so let's finish the iterator.
                break

    def __repr__( self ) -> str:
        """The string representation of the guide."""
        return f"<{self.__class__.__name__}: \"{self}\">"

    def __str__( self ) -> str:
        """The string representation of the guide.

        :returns: The guide's full path/file name.
        :rtype: str
        """
        return str( self.path.resolve() )

### guide.py ends here
