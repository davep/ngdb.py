"""Defines the class for opening and managing a Norton Guide database."""

##############################################################################
# Python imports.
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
