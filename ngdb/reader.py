"""Class for handling the low-level reading of a Norton Guide database."""

##############################################################################
# Python imports.
import io
from pathlib import Path

##############################################################################
# Low-level guide reader.
class GuideReader:
    """Low-level guide reading class."""

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

    def goto( self, pos: int ) -> None:
        """Go to a specific byte position within the guide.

        :param int pos: The position to go to.
        """
        self._h.seek( pos )

    @property
    def closed( self ) -> bool:
        """Is the file closed?

        :type: bool
        """
        return self._h.closed

    def skip( self, count: int=1 ) -> None:
        """Skip a number of bytes in the guide.

        :param int count: The optional number of bytes to skip.

        **NOTE:** If ``count`` isn't supplied then 1 byte is skilled.
        """
        self._h.seek( count, io.SEEK_CUR )

    def skip_entry( self ) -> None:
        """Skip a whole entry in the guide."""
        self.skip( self.read_word() + 22 )

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

    @staticmethod
    def _nul_trim( string: str ) -> str:
        """Trim a string from the first nul.

        :param str string: The string to trim.
        :returns: Everything up to but not including the first nul.
        :rtype: str
        """
        nul = string.find( "\000" )
        return string[ 0:nul ] if nul != -1 else string

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

### reader.py ends here
