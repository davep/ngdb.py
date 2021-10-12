"""Unit tests relating to basic guide navigation."""

##############################################################################
# Python imports.
from unittest import TestCase

##############################################################################
# Library imports.
from ngdb import NortonGuide, Short, Long

##############################################################################
# Local imports.
from . import BIG_GUIDE

##############################################################################
# Guide navigation unit tests.
class TestNavigation( TestCase ):
    """Basic guide navigation unit tests."""

    def setUp( self ) -> None:
        """Set up for the tests."""
        self.guide = NortonGuide( BIG_GUIDE )

    def test_go_first( self ) -> None:
        """It should be possible to go to the first entry."""
        self.assertIsInstance( self.guide.goto_first().load(), Short )

    def test_skip( self ) -> None:
        """It should be possible to skip an entry without reading it."""
        self.assertIsInstance( self.guide.goto_first().skip().load(), Long )

### test_navigation.py ends here
