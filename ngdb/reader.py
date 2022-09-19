"""Class for handling the low-level reading of a Norton Guide database."""

##############################################################################
# Python imports.
import io
from pathlib import Path
from typing  import Final

##############################################################################
# Low-level guide reader.
class GuideReader:
    """Low-level guide reading class.

    **NOTE:** For now, no optimisation has taken place, in many cases the
    way this class reads data from a guide will be a method that's on the
    slower side. This is on purpose; it's about readable code that
    represents the underlying data structure rather than the fastest method
    of getting data into memory.

    Once the rest of the library is done and working well this extra bit if
    docstring will likely be removed because work to improve the speed of
    this class will finally take place.
    """

    #: The value that marks run-length-encoded spaces.
    RLE_MARKER: Final = "\xFF"

    @classmethod
    def unrle( cls, rle_text: str ) -> str:
        """Un-run-length-encode the given string.

        :param str rle_text: The text that needs expanding.
        :returns: The given text with all RLE components expanded.
        :rtype: str

        Norton Guide database files use a very simple form of
        run-length-encoding for spaces. Simply put, if you find a byte in a
        string that is 0xFF, then the next byte is the number of spaces to
        insert into the string at this point. I've also found that 0xFF
        followed by 0xFF seems to mean you should insert a literal 0xFF (I
        think), although I've found that using a literal space makes more
        sense.
        """

        expanded = ""
        start    = 0
        split    = rle_text.find( cls.RLE_MARKER )

        while split > -1:
            expanded += rle_text[ start:split ] + " " * (
                1 if rle_text[ split + 1 ] == cls.RLE_MARKER else ord( rle_text[ split + 1 ] )
            )
            start = split + 2
            split = rle_text.find( cls.RLE_MARKER, start )

        return expanded + rle_text[ start: ]

    def __init__( self, guide: Path ):
        """Constructor.

        :param ~pathlib.Path guide: The guide to open.
        """
        self._h = guide.open( "rb" )

    def close( self ) -> None:
        """Close the guide."""
        self._h.close()

    @property
    def pos( self ) -> int:
        """The current position within the file.

        :type: int
        """
        return self._h.tell()

    def goto( self, pos: int ) -> "GuideReader":
        """Go to a specific byte position within the guide.

        :param int pos: The position to go to.
        :returns: self
        :rtype: GuideReader
        """
        self._h.seek( pos )
        return self

    @property
    def closed( self ) -> bool:
        """Is the file closed?

        :type: bool
        """
        return self._h.closed

    def skip( self, count: int=1 ) -> "GuideReader":
        """Skip a number of bytes in the guide.

        :param int count: The optional number of bytes to skip.
        :returns: self
        :rtype: GuideReader

        **NOTE:** If ``count`` isn't supplied then 1 byte is skilled.
        """
        self._h.seek( count, io.SEEK_CUR )
        return self

    def skip_entry( self ) -> "GuideReader":
        """Skip a whole entry in the guide.

        :returns: self
        :rtype: GuideReader
        """
        return self.skip( 2 ).skip( self.read_word() + 22 )

    @staticmethod
    def _decrypt( value: int ) -> int:
        """Decrypt a given numeric value.

        :param int value: The value to decrypt.
        :returns: The decrypted value.
        :rtype: int
        """
        return value ^ 0x1A

    def read_byte( self, decrypt: bool=True ) -> int:
        """Read a byte from the guide.

        :param bool decrypt: Should the value be decrypted?
        :returns: The byte value read.
        :rtype: int

        **NOTE:** ``decrypt`` is optional and defaults to ``True``.
        """
        buff = self._h.read( 1 )[ 0 ]
        return self._decrypt( buff ) if decrypt else buff

    def read_word( self, decrypt: bool=True ) -> int:
        """Read a two-byte word from the guide.

        :param bool decrypt: Should the value be decrypted?
        :returns: The integer value read.
        :rtype: int

        **NOTE:** ``decrypt`` is optional and defaults to ``True``.
        """
        return self.read_byte( decrypt ) + ( self.read_byte( decrypt ) << 8 )

    def peek_word( self, decrypt: bool=True ) -> int:
        """Read a two-byte word but don't move the file location.

        :param bool decrypt: Should the value be decrypted?
        :returns: The integer value read.
        :rtype: int

        **NOTE:** ``decrypt`` is optional and defaults to ``True``.
        """
        try:
            return self.read_word( decrypt )
        finally:
            self.skip( -2 )

    def read_long( self, decrypt: bool=True ) -> int:
        """Read a four-byte long word from the guide.

        :param bool decrypt: Should the value be decrypted?
        :returns: The long integer value read.
        :rtype: int

        **NOTE:** ``decrypt`` is optional and defaults to ``True``.
        """
        return self.read_word( decrypt ) + ( self.read_word( decrypt ) << 16 )

    def read_offset( self ) -> int:
        """Read an offset value from the guide.

        :returns: The offset value read.
        :rtype: int

        **NOTE:** This function ensures that an offset value that means
        'there is no offset' returns as ``-1``.
        """
        return -1 if ( offset := self.read_long( True ) ) == 0xFFFFFFFF else offset

    @staticmethod
    def _nul_trim( string: str ) -> str:
        """Trim a string from the first nul.

        :param str string: The string to trim.
        :returns: Everything up to but not including the first nul.
        :rtype: str
        """
        return string[ 0:nul ] if ( nul := string.find( "\000" ) ) != -1 else string

    def read_str( self, length: int, decrypt: bool=True ) -> str:
        """Read a fixed-length string from the guide.

        :param int length: The length of the string to read.
        :param bool decrypt: Should the string be decrypted?
        :returns: The string value read.
        :rtype: str

        **NOTE:** ``decrypt`` is optional and defaults to ``True``.
        """
        return self._nul_trim( "".join(
            chr( self._decrypt( n ) if decrypt else n ) for n in tuple( self._h.read( length ) )
        ) )

    def read_strz( self, length: int, decrypt: bool=True ) -> str:
        """Read a nul-terminated string from the guide.

        :param int length: The maximum length of the string to read.
        :param bool decrypt: Should the string be decrypted?
        :returns: The string value read.
        :rtype: str

        **NOTE:** ``decrypt`` is optional and defaults to ``True``.
        """
        # Remember where we are before we read in the string.
        pos = self.pos
        # Now read in the string.
        buff = self.read_str( length, decrypt )
        # Now skip to the location where the nul was found.
        self.goto( pos + len( buff ) + 1 )
        # Return the string.
        return buff

### reader.py ends here
