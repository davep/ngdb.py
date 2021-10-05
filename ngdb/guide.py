"""Defines the class for opening and managing a Norton Guide database."""

##############################################################################
# Python imports.
import io
from pathlib import Path
from typing  import Union

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

    def __init__( self, guide: Union[ str, Path ] ) -> None:
        """Constructor.

        :param Union[str,~pathlib.Path] guide: The guide to open.
        """

        # Remember the guide path.
        self.path = Path( guide )

        # Attempt to open the guide. Note that we're going to hold it open
        # until we're asked to close it in the close method, so we also
        # nicely ask pylint to hush.
        self._guide = self.path.open( "rb" )

        # Now, having opened it fine, read in the header.
        self._read_header()

    def _skip( self, count: int ) -> None:
        """Skip a number of bytes in the guide.

        :param int count: The number of bytes to skip.
        """
        self._guide.seek( count, io.SEEK_CUR )

    @staticmethod
    def _decrypt( value: int ) -> int:
        """Decrypt a given numeric value.

        :param int value: The value to decrypt.
        :returns: The decrypted value.
        :rtype: int
        """
        return value ^ 0x1A

    def _read_byte( self, decrypt: bool=True ) -> int:
        """Read a byte from the guide.

        :param bool decrypt: Should the value be decrypted?
        :returns: The byte value read.
        :rtype: int

        **NOTE:** ``decrypt`` is optional and defaults to ``True``.
        """
        buff = self._guide.read( 1 )[ 0 ]
        return self._decrypt( buff ) if decrypt else buff

    def _read_word( self, decrypt: bool=True ) -> int:
        """Read a two-byte word from the guide.

        :param bool decrypt: Should the value be decrypted?
        :returns: The integer value read.
        :rtype: int

        **NOTE:** ``decrypt`` is optional and defaults to ``True``.
        """
        return self._read_byte( decrypt ) + ( self._read_byte( decrypt ) << 8 )

    def _read_header( self ) -> None:
        """Read the header of the Norton Guide database."""

        # The reader is at the start of the file, so ensure that's where we
        # are.
        self._guide.seek( 0 )

        # First two bytes are the magic.
        self._magic = self._guide.read( 2 )

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
        return self._magic.decode() in self.MAGIC

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

### guide.py ends here
