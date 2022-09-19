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
from . import BIG_GUIDE

##############################################################################
# Test the loading of a guide's menu.
class TestMenuViaShort( TestCase ):
    """Norton Guide menu unit tests."""

    def setUp( self ) -> None:
        """Set up for the tests."""
        self.guide = NortonGuide( BIG_GUIDE )

    def test_has_menus( self ) -> None:
        """The test guide has the correct number of menus."""
        self.assertEqual( self.guide.menu_count, 1 )
        self.assertEqual( self.guide.menu_count, len( self.guide.menus ) )
        self.assertTrue( all( isinstance( menu, Menu ) for menu in self.guide.menus ) )

    def test_menu_title( self ) -> None:
        """The menu title should load correctly."""
        self.assertEqual( self.guide.menus[ 0 ].title, "OSLIB" )
        self.assertEqual( self.guide.menus[ 0 ].title, str( self.guide.menus[ 0 ] ) )

    def test_menu_options( self ) -> None:
        """The menu options should load correctly."""
        self.assertCountEqual(
            self.guide.menus[ 0 ].prompts,
            [ "Functions", "FAQs", "Revision History", "Credits", "About" ]
        )
        self.assertCountEqual(
            [ prompt.prompt for prompt in self.guide.menus[ 0 ] ],
            [ "Functions", "FAQs", "Revision History", "Credits", "About" ]
        )

    def test_menu_item( self ) -> None:
        """It should be possible to treat a menu like a list."""
        self.assertEqual( self.guide.menus[ 0 ][ 0 ][ 0 ], "Functions" )
        self.assertEqual( self.guide.menus[ 0 ][ 0 ].prompt, "Functions" )

### test_guide_menu.py ends here
