"""Norton Guide entry content markup unit tests."""

##############################################################################
# Python imports.
from unittest import TestCase

##############################################################################
# Library imports.
from ngdb import PlainText

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

### test_parser.py ends here
