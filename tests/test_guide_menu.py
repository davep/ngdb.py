"""Guide menu unit tests."""

##############################################################################
# Python imports.
from unittest import TestCase

##############################################################################
# Library imports.
from ngdb      import NortonGuide
from ngdb.menu import Menu

##############################################################################
# Local imports.
from . import GOOD_GUIDE

##############################################################################
# Test the loading of a guide's menu.
class TestMenu( TestCase ):
    """Norton Guide menu unit tests."""

    def setUp( self ) -> None:
        """Set up for the tests."""
        self.guide = NortonGuide( GOOD_GUIDE )

    def test_has_menu_object( self ) -> None:
        """The test guide should have a menu object."""
        self.assertGreater( len( self.guide.menus ), 0 )
        self.assertTrue( all( isinstance( value, Menu ) for value in self.guide.menus ) )

### test_guide_menu.py ends here
