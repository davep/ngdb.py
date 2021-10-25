"""Norton Guide entry content markup unit tests."""

##############################################################################
# Python imports.
from typing   import List, Union, Tuple, Any, Iterator
from unittest import TestCase

##############################################################################
# Library imports.
from ngdb import BaseParser, PlainText

##############################################################################
# Plain text parser tests.
class TestPlainText( TestCase ):
    """Perform parser tests against the plain text parser."""

    def test_empty_string( self ) -> None:
        """It can handle an empty line."""
        self.assertEqual( str( PlainText( "" ) ), "" )

    def test_no_markup( self ) -> None:
        """It can handle a line with no markup."""
        self.assertEqual( str( PlainText( "Test" ) ), "Test" )

    def test_strips_non_text_markup( self ) -> None:
        """It should strip all non-text markup without issue."""
        self.assertEqual(
            str( PlainText( "^A10This ^Bis ^Na ^Rtest, ^Ureally it is." ) ),
            "This is a test, really it is."
        )

    def test_strips_only_non_text_markup( self ) -> None:
        """It should turn non-text markup only into an empty string."""
        self.assertEqual( str( PlainText( "^A10^B^N^R^U" ) ), "" )

    def test_ctrl_ctrl( self ) -> None:
        """^^ should become ^."""
        self.assertEqual( str( PlainText( "^^" * 10 ) ), "^" * 10 )

    def test_char_code( self ) -> None:
        """It should be able to handle character codes."""
        self.assertEqual( str( PlainText( "^C20^C21" ) ), " !" )

    def test_truncated_markup( self ) -> None:
        """It should handle truncated markup."""
        self.assertEqual( str( PlainText( "^" ) ), "" )

##############################################################################
#: Type of a single event that the TestParser will catch.
TEvent = Union[ str, Tuple[ str, Any ] ]

##############################################################################
#: Type of the collection of events in the TestParser.
TEvents = List[ TEvent ]

##############################################################################
# Unit-test-oriented Norton Guide line parser.
class TestParser( BaseParser ):
    """Parser class for working with unit tests."""

    def __init__( self, line: str ) -> None:
        """Constructor."""

        # First off, we're going to collect all the different events that
        # happen, so start a list for doing that.
        self._events: TEvents = []

        # Then call the super.
        super().__init__( line )

    def text( self, text: str ) -> None:
        """Handle the given text.

        :param str text: The text to handle.
        """
        self._events.append( ( "T", text ) )

    def colour( self, colour: int ) -> None:
        """Handle the given colour value.

        :param int colour: The colour value to handle.
        """
        self._events.append( ( "A", colour ) )

    def normal( self ) -> None:
        """Handle being asked to go to normal mode."""
        self._events.append( "N" )

    def bold( self ) -> None:
        """Handle being asked to go to bold mode."""
        self._events.append( "B" )

    def unbold( self ) -> None:
        """Handle being asked to go out of bold mode."""
        self._events.append( "b" )

    def reverse( self ) -> None:
        """Handle being asked to go to reverse mode."""
        self._events.append( "R" )

    def unreverse( self ) -> None:
        """Handle being asked to go out of reverse mode."""
        self._events.append( "r" )

    def underline( self ) -> None:
        """Handle being asked to go in underline mode."""
        self._events.append( "U" )

    def ununderline( self ) -> None:
        """Handle being asked to go out of underline mode."""
        self._events.append( "u" )

    def char( self, char: int ) -> None:
        """Handle an individual character value.

        :param int char: The character value to handle.
        """
        self._events.append( ( "C", char ) )

    def __iter__( self ) -> Iterator[ TEvent ]:
        """The collection of events caught by the parser."""
        return iter( self._events )

##############################################################################
# Parser event unit tests.
class TestParseEvents( TestCase ):
    """Test the various events that happen within a parser."""

    def test_empty_line( self ) -> None:
        """There should be no events in an empty line."""
        self.assertListEqual( list( TestParser( "" ) ), [] )

    def test_no_markup( self ) -> None:
        """There should be a single text event for a non-markup line."""
        self.assertListEqual( list( TestParser( "Hello, World!" ) ), [ ( "T", "Hello, World!" ) ] )

    def test_colour( self ) -> None:
        """There should be a colour event when there's a ^A."""
        self.assertListEqual(
            list( TestParser( "Hello, ^A20World!" ) ),
            [
                ( "T", "Hello, " ),
                ( "A", 0x20 ),
                ( "T", "World!" )
            ]
        )

    def test_multi_colour( self ) -> None:
        """Multiple there should be multiple colour events with multiple ^A."""
        self.assertListEqual(
            list( TestParser( "Hello, ^A20World^A64!" ) ),
            [
                ( "T", "Hello, " ),
                ( "A", 0x20 ),
                ( "T", "World" ),
                ( "A", 0x64 ),
                ( "T", "!" )
            ]
        )

    def test_same_colour( self ) -> None:
        """Two consecutive ^A of the same colour should cause a ^N."""
        self.assertListEqual(
            list( TestParser( "Hello, ^A20World^A20!" ) ),
            [
                ( "T", "Hello, " ),
                ( "A", 0x20 ),
                ( "T", "World" ),
                "N",
                ( "T", "!" )
            ]
        )

    def test_bold( self ) -> None:
        """It should be possible to turn bold on and off with ^B."""
        self.assertListEqual(
            list( TestParser( "Hello, ^BWorld^B!" ) ),
            [
                ( "T", "Hello, " ),
                "B",
                ( "T", "World" ),
                "b",
                ( "T", "!" )
            ]
        )

    def test_char( self ) -> None:
        """It should be possible to generate characters with ^C."""
        self.assertListEqual(
            list( TestParser( "".join( f"^C{n:02x}" for n in range( 256 ) ) ) ),
            [ ( "C", n ) for n in range( 256 ) ]
        )

    def test_normal( self ) -> None:
        """A ^N markup should result in a back-to-normal event."""
        self.assertListEqual(
            list( TestParser( "Hello, ^NWorld!" ) ),
            [
                ( "T", "Hello, " ),
                "N",
                ( "T", "World!" ),
            ]
        )

    def test_reverse( self ) -> None:
        """It should be possible to turn reverse on and off with ^R."""
        self.assertListEqual(
            list( TestParser( "Hello, ^RWorld^R!" ) ),
            [
                ( "T", "Hello, " ),
                "R",
                ( "T", "World" ),
                "r",
                ( "T", "!" )
            ]
        )

    def test_underline( self ) -> None:
        """It should be possible to turn underline on and off with ^U."""
        self.assertListEqual(
            list( TestParser( "Hello, ^UWorld^U!" ) ),
            [
                ( "T", "Hello, " ),
                "U",
                ( "T", "World" ),
                "u",
                ( "T", "!" )
            ]
        )

### test_parser.py ends here
