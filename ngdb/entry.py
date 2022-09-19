"""Norton guide entry loading and holding code."""

##############################################################################
# Python imports.
from typing import Type, Dict, Callable, Tuple, Iterator, NamedTuple

##############################################################################
# Local imports.
from .reader  import GuideReader
from .types   import EntryType, UnknownEntryType
from .seealso import SeeAlso

##############################################################################
# Loads and holds entry parent information.
class EntryParent:
    """Class to load and hold the parent information for an entry."""

    def __init__( self, guide: GuideReader ) -> None:
        """Constructor.

        :param GuideReader guide: The reader object for the guide.
        """
        self._line   = guide.read_word()
        self._offset = guide.read_offset()
        self._menu   = guide.read_word()
        self._prompt = guide.read_word()

    @property
    def offset( self ) -> int:
        """The offset of the parent entry, if there is one.

        :type: int
        """
        return self._offset

    def __bool__( self ) -> bool:
        """Is there a parent entry?

        :returns: ``True`` if there is, ``False` if not.
        :rtype: bool
        """
        return self.offset > 0

    @staticmethod
    def _non_test( value: int ) -> int:
        """Ensure a -1 is a -1."""
        return -1 if value == 0xFFFF else value

    @property
    def line( self ) -> int:
        """The line in the parent entry that point to this entry.

        :type: int

        If there is no parent line this will be ``-1``. But also see
        ``has_line`` for a test for a parent entry line.
        """
        return self._non_test( self._line )

    @property
    def has_line( self ) -> int:
        """Does this entry have a parent entry line that points to it?

        :type: bool
        """
        return self.line != -1

    @property
    def menu( self ) -> int:
        """The menu that relates to this entry.

        :type: int

        If there is no menu, this will be ``-1``. But also see ``has_menu``
        to test if there is a related menu.
        """
        return self._non_test( self._menu )

    @property
    def has_menu( self ) -> bool:
        """Is there a menu related to this entry?

        :type: bool
        """
        return self.menu != -1

    @property
    def prompt( self ) -> int:
        """The menu prompt related to this entry.

        :type: int

        If there is no menu prompt, this will be ``-1``. But also see
        ``has_prompt`` to test if there is a related menu prompt.
        """
        return self._non_test( self._prompt )

    @property
    def has_prompt( self ) -> bool:
        """Is there a menu prompt related to this entry?

        :type: bool
        """
        return self.has_menu and self.prompt != -1

##############################################################################
#: Type of the type of an entry.
TEntry = Type[ "Entry" ]

##############################################################################
#: Maximum size of a line we'll look for in a guide.
MAX_LINE_LENGTH = 1024

##############################################################################
# Guide entry class.
class Entry:
    """Norton Guide database entry class."""

    #: Holds the entry type mapper.
    _map: Dict[ EntryType, TEntry ] = {}

    @classmethod
    def loads( cls, entry_type: EntryType ) -> Callable[ [ TEntry ], TEntry ]:
        """Decorator for defining which class handles which entry type.

        :param EntryType entry_type: The ID of the entry type being handled.
        :returns: The decorator wrapper.
        :rtype: Callable[[TEntry],TEntry]
        """
        def _register( handler: TEntry ) -> TEntry:
            """Inner decorator function."""
            cls._map[ entry_type ] = handler
            return handler
        return _register

    @classmethod
    def load( cls, guide: GuideReader ) -> "Entry":
        """Load the entry at the current position in the guide.

        :param GuideReader guide: The reader object for the guide.
        :returns: The correct type of entry object.
        :rtype: Entry
        :raises ~.types.UnknownEntryType: Indicates that the entry type is unknown.
        """
        try:
            return cls._map[ EntryType( guide.peek_word() ) ]( guide )
        except ( ValueError, KeyError ) as error:
            raise UnknownEntryType( f"Unknown guide entry type: {guide.peek_word()}" ) from error

    def __init__( self, guide: GuideReader ) -> None:
        """Constructor.

        :param GuideReader guide: The reader object for the guide.
        """

        # Load up the main details for the entry.
        self._offset        = guide.pos
        self._type          = guide.read_word()
        self._size          = guide.read_word()
        self._line_count    = guide.read_word()
        self._has_see_also  = guide.read_word()
        self._parent        = EntryParent( guide )
        self._previous      = guide.read_offset()
        self._next          = guide.read_offset()

        # Set up for loading in the lines.
        self._lines: Tuple[ str, ... ] = ()

    def _load_lines( self, guide: GuideReader ) -> None:
        """Load in all of the lines of text, from this point.

        :param GuideReader guide: The reader object for the guide.
        """
        self._lines = tuple(
            guide.unrle( guide.read_strz( MAX_LINE_LENGTH ) ) for _ in range( len( self ) )
        )

    @property
    def offset( self ) -> int:
        """The file offset of this entry.

        :type: int
        """
        return self._offset

    @property
    def type_id( self ) -> int:
        """The numeric ID of the type of entry.

        :type: int
        """
        return self._type

    @property
    def size( self ) -> int:
        """The size of the entry in bytes.

        :type: int
        """
        return self._size

    def __len__( self ) -> int:
        """The number of lines in the entry.

        :returns: The number of lines.
        :rtype: int
        """
        return self._line_count

    @property
    def has_see_also( self ) -> bool:
        """Does this entry have any see-also items?

        :type: bool
        """
        return self._has_see_also > 0

    @property
    def parent( self ) -> EntryParent:
        """Returns the parent entry information.

        :type: EntryParent
        """
        return self._parent

    @property
    def previous( self ) -> int:
        """The location of the previous entry.

        :type: int
        """
        return self._previous

    @property
    def has_previous( self ) -> bool:
        """Is there a previous entry?

        :type: bool
        """
        return self.previous > 0

    @property
    def next( self ) -> int:
        """The location of the next entry.

        :type: int
        """
        return self._next

    @property
    def has_next( self ) -> bool:
        """Is there a previous entry?

        :type: bool
        """
        return self.next > 0

    @property
    def lines( self ) -> Tuple[ str, ... ]:
        """The lines of text in the entry.

        :type: Tuple[str,...]
        """
        return self._lines

    def __str__( self ) -> str:
        """Return the text of the entry as a single string.

        :returns: The entry's text.
        :rtype: str
        """
        return "\n".join( self.lines )

    def __repr__( self ) -> str:
        """Simply say the type of entry as the representation of the object.

        :returns: The name of the type of entry.
        :rtype: str
        """
        return f"<{self.__class__.__name__}: {self.offset}>"

##############################################################################
# Short entry class.
@Entry.loads( EntryType.SHORT )
class Short( Entry ):
    """Short Norton Guide database entry."""

    def __init__( self, guide: GuideReader ) -> None:
        """Constructor.

        :param GuideReader guide: The reader object for the guide.
        """

        # Call the super class.
        super().__init__( guide )

        # Next up, load up all of the offsets associated with each of the
        # lines in the entry.
        self._offsets = tuple( self._load_offsets( guide ) )

        # Finally, load in the actual text.
        self._load_lines( guide )

    def _load_offsets( self, guide: GuideReader ) -> Iterator[ int ]:
        """Load up the offsets for each of the lines in the entry.

        :param GuideReader guide: The reader object for the guide.
        :yields: int
        """
        for _ in range( len( self ) ):
            # Skip a word -- I don't know what this is.
            guide.skip( 2 )
            # Read the offset of the line.
            yield guide.read_offset()

    @property
    def offsets( self ) -> Tuple[ int, ... ]:
        """The offsets for each of the lines in the entry.

        :type: Tuple[int,...]
        """
        return self._offsets

    class Line( NamedTuple ):
        """Named tuple that holds details of a line in a short entry."""

        #: The text of the line.
        text: str
        #: The offset that the line points to.
        offset: int

        @property
        def has_offset( self ) -> bool:
            """Does this line have an associated offset into the file?

            :type: bool
            """
            return self.offset > 0

    def __getitem__( self, line: int ) -> Line:
        """Get a line and its offset."""
        return self.Line( self.lines[ line ], self.offsets[ line ] )

    def __iter__( self ) -> Iterator[ Line ]:
        """The lines in the entry along with the offsets into the guide."""
        return ( self.Line( *line ) for line in zip( self.lines, self.offsets ) )

##############################################################################
# Long entry class.
@Entry.loads( EntryType.LONG )
class Long( Entry ):
    """Long Norton Guide database entry."""

    def __init__( self, guide: GuideReader ) -> None:
        """Constructor.

        :param GuideReader guide: The reader object for the guide.
        """

        # Call the super class.
        super().__init__( guide )

        # Load in the actual text.
        self._load_lines( guide )

        # Load up the see-also information.
        self._see_also = SeeAlso( guide, self.has_see_also )

    @property
    def see_also( self ) -> SeeAlso:
        """The see-also information for this entry.

        :type: SeeAlso
        """
        return self._see_also

    def __getitem__( self, line: int ) -> str:
        """Get a line from the entry."""
        return self.lines[ line ]

    def __iter__( self ) -> Iterator[ str ]:
        """The lines in the entry."""
        return iter( self.lines )

### entry.py ends here
