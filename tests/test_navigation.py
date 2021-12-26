"""Unit tests relating to basic guide navigation."""

##############################################################################
# Python imports.
from unittest import TestCase

##############################################################################
# Library imports.
from ngdb import NortonGuide, Short, Long, NGEOF

##############################################################################
# Local imports.
from . import GOOD_GUIDE, BIG_GUIDE

##############################################################################
# Guide navigation unit tests.
class TestBasicNavigation( TestCase ):
    """Basic guide navigation unit tests."""

    def setUp( self ) -> None:
        """Set up for the tests."""
        self.guide = NortonGuide( BIG_GUIDE )

    def test_go_first( self ) -> None:
        """It should be possible to go to the first entry."""
        self.assertIsInstance( NortonGuide( BIG_GUIDE ).goto_first().load(), Short )

    def test_skip( self ) -> None:
        """It should be possible to skip an entry without reading it."""
        self.assertIsInstance( NortonGuide( BIG_GUIDE ).goto_first().skip().load(), Long )

##############################################################################
# EOF detection tests.
class TestEOF( TestCase ):
    """Unit tests relating to detecting EOF in a guide."""

    def test_small_eof_skip( self ) -> None:
        """A guide with one entry should EOF when skipping."""
        guide = NortonGuide( GOOD_GUIDE )
        guide.skip()
        self.assertTrue( guide.eof )

    def test_small_eof_load( self ) -> None:
        """A guide with one entry should not EOF when loading."""
        guide = NortonGuide( GOOD_GUIDE )
        guide.load()
        self.assertFalse( guide.eof )

    def test_big_eof_skip( self ) -> None:
        """A guide with multiple entries should not be EOF early on during skips."""
        guide = NortonGuide( BIG_GUIDE ).goto_first()
        for _ in range( 5 ):
            guide.skip()
            self.assertFalse( guide.eof )

    def test_big_eof_load( self ) -> None:
        """A guide with multiple entries should not be EOF early on during loads."""
        guide = NortonGuide( BIG_GUIDE ).goto_first()
        for _ in range( 5 ):
            guide.load()
            guide.skip()
            self.assertFalse( guide.eof )

    def test_small_eof_guard_skip( self ) -> None:
        """Attempting to skip past the end of single-entry guide should throw an error."""
        guide = NortonGuide( GOOD_GUIDE ).goto_first()
        with self.assertRaises( NGEOF ):
            for _ in range( 100 ):
                guide.skip()

    def test_big_eof_guard_skip( self ) -> None:
        """Attempting to skip past the end of multiple-entry guide should throw an error."""
        guide = NortonGuide( BIG_GUIDE ).goto_first()
        with self.assertRaises( NGEOF ):
            for _ in range( 100 ):
                guide.skip()

##############################################################################
# Guide iteration tests.
class TestIter( TestCase ):
    """Unit tests relating to iterating through a guide."""

    def test_iter_small( self ) -> None:
        """It should be possible to iterate through a guide with one entry."""
        self.assertEqual( len( list( NortonGuide( GOOD_GUIDE ) ) ), 1 )

    def test_iter_big( self ) -> None:
        """It should be possible to iterate through a guide with more than one entry."""
        self.assertEqual( len( list( NortonGuide( BIG_GUIDE ) ) ), 28 )

### test_navigation.py ends here
