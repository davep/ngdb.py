"""Norton Guide entry tests."""

##############################################################################
# Python imports.
from unittest import TestCase

##############################################################################
# Library imports.
from ngdb       import NortonGuide, Short, Long, UnknownEntryType
from ngdb.types import EntryType

##############################################################################
# Local imports.
from . import BIG_GUIDE

##############################################################################
# Unknown entry type tests.
class TestUnknown( TestCase ):
    """Test picking up on an unknown entry type."""

    def test_unknown( self ) -> None:
        """Attempting to load an unknown entry type should result in an exception."""
        with self.assertRaises( UnknownEntryType ):
            NortonGuide( BIG_GUIDE ).goto( 0 ).load()

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
        self.assertTrue( EntryType.is_short( self.entry.type_id ) )
        self.assertFalse( EntryType.is_long( self.entry.type_id ) )

    def test_entry_size( self ) -> None:
        """It should have the correct size."""
        self.assertEqual( self.entry.size, 838 )

    def test_parent( self ) -> None:
        """It should not have a parent."""
        self.assertFalse( bool( self.entry.parent ) )

    def test_parent_line( self ) -> None:
        """It should not have a parent line."""
        self.assertFalse( self.entry.parent.has_line )

    def test_parent_menu( self ) -> None:
        """The test short entry should have a parent menu."""
        self.assertTrue( self.entry.parent.has_menu )

    def test_parent_prompt( self ) -> None:
        """The test short entry should have a parent menu prompt."""
        self.assertTrue( self.entry.parent.has_prompt )

    def test_previous( self ) -> None:
        """It should not have a previous entry."""
        self.assertFalse( self.entry.has_previous )

    def test_next( self ) -> None:
        """It should not have a next entry."""
        self.assertFalse( self.entry.has_next )

    def test_str_entry( self ) -> None:
        """The str() of the entry should be the main text."""
        str_entry = str( self.entry )
        self.assertEqual( len( str_entry.split( "\n" ) ), len( self.entry ) )

    def test_lines_and_offsets( self ) -> None:
        """There should be equal numbers of lines and offsets."""
        self.assertEqual( len( self.entry.lines ), len( self.entry.offsets ) )

    def test_list_like( self ) -> None:
        """It should be possible to treat a short entry like a list."""
        self.assertEqual(
            self.entry[ 0 ],
            ( " OL_95AppTitle()          Set/get the Windows 95 application title.", 1389 )
        )
        self.assertEqual(
            self.entry[ 0 ].text,
            " OL_95AppTitle()          Set/get the Windows 95 application title."
        )
        self.assertEqual( self.entry[ 0 ].offset, 1389 )
        self.assertTrue( self.entry[ 0 ].has_offset )

    def test_iter_iter( self ) -> None:
        """It should be possible to treat a short entry like an iterator."""
        self.assertEqual(
            next( iter( self.entry ) ),
            ( " OL_95AppTitle()          Set/get the Windows 95 application title.", 1389 )
        )

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
        self.assertFalse( EntryType.is_short( self.entry.type_id ) )
        self.assertTrue( EntryType.is_long( self.entry.type_id ) )

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

    def test_parent_menu( self ) -> None:
        """The test long entry should have a parent menu."""
        self.assertTrue( self.entry.parent.has_menu )

    def test_parent_prompt( self ) -> None:
        """The test long entry should have a parent menu prompt."""
        self.assertTrue( self.entry.parent.has_prompt )

    def test_previous( self ) -> None:
        """It should not have a previous entry."""
        self.assertFalse( self.entry.has_previous )

    def test_next( self ) -> None:
        """It should have a next entry."""
        self.assertTrue( self.entry.has_next )

    def test_str_entry( self ) -> None:
        """The str() of the entry should be the main text."""
        str_entry = str( self.entry )
        self.assertEqual( len( str_entry.split( "\n" ) ), len( self.entry ) )

    def test_list_like( self ) -> None:
        """It should be possible to treat a long entry like a list."""
        self.assertEqual( self.entry[ 0 ], " ^bOL_95AppTitle()" )

    def test_iter_like( self ) -> None:
        """It should be possible to treat a long entry like an iterator."""
        self.assertEqual( next( iter( self.entry ) ), " ^bOL_95AppTitle()" )

    def test_see_also( self ) -> None:
        """The test long entry should have a see-also menu."""
        self.assertTrue( bool( self.entry.see_also ) )

    def test_see_also_count( self ) -> None:
        """The test long entry should have the correct number of see-also items."""
        self.assertEqual( len( self.entry.see_also ), 1 )

    def test_see_also_text( self ) -> None:
        """The test long entry should have the correct see-also prompt."""
        self.assertEqual( self.entry.see_also.prompts[ 0 ], "OL_95VMTitle()" )

    def test_see_also_offset( self ) -> None:
        """The test long entry should have the correct see-also offset."""
        self.assertEqual( self.entry.see_also.offsets[ 0 ], 2355 )

    def test_see_also_list_like( self ) -> None:
        """It should be possible to treat the see-also object like a list."""
        self.assertEqual( self.entry.see_also[ 0 ], ( "OL_95VMTitle()", 2355 ) )

    def test_see_also_iter_like( self ) -> None:
        """It should be possible to treat the see-also object like an iterator."""
        self.assertEqual( next( iter( self.entry.see_also ) ), ( "OL_95VMTitle()", 2355 ) )

### test_guide_entry.py ends here
