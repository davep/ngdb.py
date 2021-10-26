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

    def test_title( self ) -> None:
        """The title should read correctly."""
        self.assertEqual( self.guide.title, "Expert Guide" )

    def test_credits( self ) -> None:
        """The credits should read correctly."""
        self.assertCountEqual(
            self.guide.credits,
            (
                "Expert Guide",
                "Copyright (c) 1997-2015 David A. Pearson",
                "",
                "email: davep@davep.org",
                "  web: http://www.davep.org/"
            )
        )

    def test_made_with( self ) -> None:
        """The test guide should be made with the Norton Guide compiler."""
        self.assertEqual( self.guide.made_with, NortonGuide.MAGIC[ "NG" ] )

### test_guide_header.py ends here
