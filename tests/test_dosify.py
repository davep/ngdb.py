"""Library DOS-a-like utility code unit tests."""

##############################################################################
# Python imports.
from unittest import TestCase

##############################################################################
# Library imports.
from ngdb import make_dos_like

##############################################################################
# DOS-a-like text conversion unit tests.
class TestMakeDOSLike( TestCase ):
    """Test the utility function that helps with DOS character conversion."""

    def test_empty_string( self ) -> None:
        """It can handle an empty string."""
        self.assertEqual( make_dos_like( "" ), "" )

    def test_plain_string( self ) -> None:
        """It can handle some plain text."""
        self.assertEqual( make_dos_like( "Hello, World!" ), "Hello, World!" )

    def test_graphical( self ) -> None:
        """It can handle some \"graphical\" characters."""
        self.assertEqual( make_dos_like( "Ä" * 100 ), "─" * 100 )

### test_dosify.py ends here
