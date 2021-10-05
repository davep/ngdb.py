"""Test the main header reading code."""

##############################################################################
# Python imports.
from unittest import TestCase

##############################################################################
# Library imports.
from ngdb import NortonGuide

##############################################################################
# Local imports.
from . import GOOD_GUIDE

##############################################################################
# Test various attributes of a Norton Guide database header.
class TestGoodHeader( TestCase ):
    """Good Norton Guide database header tests."""

    def setUp( self ) -> None:
        """Set up for the tests."""
        self.guide = NortonGuide( GOOD_GUIDE )

    def test_is_ng( self ) -> None:
        """It should be possible to test for a valid database."""
        self.assertTrue( self.guide.is_a )

    def test_menu_count( self ) -> None:
        """The menu count should read correctly."""
        self.assertEqual( self.guide.menu_count, 1 )

### test_guide_header.py ends here
