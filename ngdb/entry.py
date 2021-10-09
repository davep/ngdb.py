"""Norton guide entry loading and holding code."""

##############################################################################
# Python imports.
from typing import Type, Dict, Callable

##############################################################################
# Local imports.
from .reader import GuideReader
from .types  import EntryType

##############################################################################
# Loads and holds entry parent information.
class EntryParent:
    """Class to load and hold the parent information for an entry."""

    def __init__( self, guide: GuideReader ) -> None:
        """Constructor.

        :param GuideReader guide: The reader object for the guide.
        """
        self._offset = guide.read_long()
        self._line   = guide.read_word()
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
        return self.offset != -1

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
        """
        if ( entry_type := EntryType( guide.peek_word() ) ) in cls._map:
            return cls._map[ entry_type ]( guide )
        # TODO: Custom exception type.
        raise Exception( "Unknown guide type" )

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
        self._previous      = guide.read_long()
        self._next          = guide.read_long()

        # TODO: Read actual text.

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

##############################################################################
# Short entry class.
@Entry.loads( EntryType.SHORT )
class Short( Entry ):
    """Short Norton Guide databsae entry."""

##############################################################################
# Long entry class.
@Entry.loads( EntryType.LONG )
class Long( Entry ):
    """Long Norton Guide databsae entry."""

### entry.py ends here
