"""Norton Guide entry tests."""

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
# Test loading up a short entry.
class TestShort( TestCase ):
    """Short entry loading unit tests."""

    def setUp( self ) -> None:
        """Set up for testing the short entry."""
        self.entry = NortonGuide( BIG_GUIDE ).goto_first().load()

    def test_load_correct_type( self ) -> None:
        """A short entry should load as the correct type."""
        self.assertIsInstance( self.entry, Short )

    def test_correct_id( self ) -> None:
        """It should have a short entry ID."""
        self.assertEqual( self.entry.type_id, 0 )

    def test_entry_size( self ) -> None:
        """It should have the correct size."""
        self.assertEqual( self.entry.size, 838 )

    def test_parent( self ) -> None:
        """It should not have a parent."""
        self.assertFalse( bool( self.entry.parent ) )

    def test_parent_line( self ) -> None:
        """It should not have a parent line."""
        self.assertFalse( self.entry.parent.has_line )

##############################################################################
# Test loading up a long entry.
class TestLong( TestCase ):
    """Long entry loading unit tests."""

    def setUp( self ) -> None:
        """Set up for testing the long entry."""
        self.entry = NortonGuide( BIG_GUIDE ).goto_first().skip().load()

    def test_load_correct_type( self ) -> None:
        """A long entry should load as the correct type."""
        self.assertIsInstance( self.entry, Long )

    def test_correct_id( self ) -> None:
        """It should have a long entry ID."""
        self.assertEqual( self.entry.type_id, 1 )

    def test_entry_size( self ) -> None:
        """It should have the correct size."""
        self.assertEqual( self.entry.size, 940 )

    def test_parent( self ) -> None:
        """It should have a parent."""
        self.assertTrue( bool( self.entry.parent ) )

    def test_parent_line( self ) -> None:
        """It should have a parent line."""
        self.assertTrue( self.entry.parent.has_line )
        self.assertEqual( self.entry.parent.line, 0 )

### test_guide_entry.py ends here
