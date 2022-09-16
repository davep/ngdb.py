"""Norton Guide parser for the text inside a guide."""

##############################################################################
# Python imports.
from typing import Final
from enum   import Enum, auto

##############################################################################
# Enumerated text modes for line parsing.
class TextMode( Enum ):
    """Types of text mode used when parsing a Norton Guide line."""
    NORMAL    = auto()
    BOLD      = auto()
    UNDERLINE = auto()
    REVERSE   = auto()
    ATTR      = auto()

##############################################################################
#: The control character that marks an upcoming attribute.
CTRL_CHAR: Final = "^"

##############################################################################
# Class to help track the state of raw parsing.
class ParseState:
    """Raw text parsing state tracking class.

    :ivar int ctrl: The location of the next control marker.
    :ivar str raw: The current raw text that's left to handle.
    :ivar TextMode mode: The current mode.
    :ivar int last_attr: The last attribute encountered.
    """

    def __init__( self, line: str ) -> None:
        """Constructor.

        :param str line: The line to work on.
        """
        self.raw       = line
        self.ctrl      = line.find( CTRL_CHAR )
        self.mode      = TextMode.NORMAL
        self.last_attr = -1

    @property
    def work_left( self ) -> bool:
        """Is there any work left to do?

        :type: bool
        """
        return self.ctrl != -1 and self.ctrl < len( self.raw )

    @property
    def ctrl_id( self ) -> str:
        """The current control ID.

        :type: str
        """
        try:
            return self.raw[ self.ctrl + 1 ].lower()
        except IndexError:
            # If we've fallen in here, it's mostly because we've run into
            # some situation where there's a lone ^ at the end of the line.
            # This feels like a detail that the user-level code should not
            # be having to faff with. I feel that, as much as possible, the
            # parsing code should do its absolute best to return something
            # readable when faced with invalid markup.
            return ""

##############################################################################
# Base parser class.
class BaseParser:
    """The base text parsing class."""

    def __init__( self, line: str ) -> None:
        """Constructor.

        :param str line: The raw string to parse.
        """

        # State tracker.
        state = ParseState( line )

        # While we've not run out of text to process...
        while state.work_left:

            # If there was text between the last markup and the next...
            if len( state.raw[ :state.ctrl ] ) > 0:
                # ...handle it.
                self.text( state.raw[ :state.ctrl ] )

            # Pull out the character following the control character and
            # handle it.
            if ( ctrl := state.ctrl_id ) == CTRL_CHAR:
                # We're looking at ^^, which is a ^.
                self.text( CTRL_CHAR )
                state.ctrl += 2
            elif hasattr( self, f"_ctrl_{ctrl}" ):
                # Looks like we can handle whatever's there, so dispatch
                # it...
                getattr( self, f"_ctrl_{ctrl}" )( state )
            else:
                # No idea what the next character is. We could either raise
                # an exception, eat the next character, or simply skip along
                # one. For now, let's just skip along one.
                state.ctrl += 1

            # Chop the bits we've done off the raw string.
            state.raw = state.raw[ state.ctrl: ]

            # Find the next control character.
            state.ctrl = state.raw.find( CTRL_CHAR )

        # Handle any remaining text.
        if len( state.raw ) > 0:
            self.text( state.raw )

    def _ctrl_a( self, state: ParseState ) -> None:
        """Handle ^A markup.

        :param ParseState state: The data that tracks parse state.
        """

        # Get the actual attribute.
        attr = int( state.raw[ state.ctrl+2:state.ctrl+4 ], 16 )

        # If there's already a colour attribute in effect and the
        # new colour is the same as the previous colour...
        if state.mode is TextMode.ATTR and attr == state.last_attr:
            # ...that means it's a return to "normal".
            self.normal()
            state.mode = TextMode.NORMAL
        else:
            # ...otherwise we start a colour attribute.
            self.colour( attr )
            state.last_attr = attr
            state.mode      = TextMode.ATTR

        # Skip.
        state.ctrl += 4

    def _ctrl_b( self, state: ParseState ) -> None:
        """Handle ^B markup.

        :param ParseState state: The data that tracks parse state.
        """

        # If we're in bold mode...
        if state.mode is TextMode.BOLD:
            # ...go back to normal.
            self.unbold()
            state.mode = TextMode.NORMAL
        else:
            # ...otherwise go bold!
            self.bold()
            state.mode = TextMode.BOLD

        # Skip!
        state.ctrl += 2

    def _ctrl_c( self, state: ParseState ) -> None:
        """Handle ^C markup.

        :param ParseState state: The data that tracks parse state.
        """
        self.char( int( state.raw[ state.ctrl+2:state.ctrl+4 ], 16 ) )
        state.ctrl += 4

    def _ctrl_n( self, state: ParseState ) -> None:
        """Handle ^N markup.

        :param ParseState state: The data that tracks parse state.
        """
        self.normal()
        state.mode = TextMode.NORMAL
        state.ctrl += 2

    def _ctrl_r( self, state: ParseState ) -> None:
        """Handle ^R markup.

        :param ParseState state: The data that tracks parse state.
        """

        # If we're in reverse mode...
        if state.mode is TextMode.REVERSE:
            # ...go back to normal.
            self.unreverse()
            state.mode = TextMode.NORMAL
        else:
            # ...otherwise go reverse.
            self.reverse()
            state.mode = TextMode.REVERSE

        # Skip!
        state.ctrl += 2

    def _ctrl_u( self, state: ParseState ) -> None:
        """Handle ^U markup.

        :param ParseState state: The data that tracks parse state.
        """

        # If we're in underline mode...
        if state.mode is TextMode.UNDERLINE:
            # ...go back to normal.
            self.ununderline()
            state.mode = TextMode.NORMAL
        else:
            # ...otherwise go underline.
            self.underline()
            state.mode = TextMode.UNDERLINE

        # Skip!
        state.ctrl += 2

    def text( self, text: str ) -> None:
        """Handle the given text.

        :param str text: The text to handle.
        """

    def colour( self, colour: int ) -> None:
        """Handle the given colour value.

        :param int colour: The colour value to handle.
        """

    def normal( self ) -> None:
        """Handle being asked to go to normal mode."""

    def bold( self ) -> None:
        """Handle being asked to go to bold mode."""

    def unbold( self ) -> None:
        """Handle being asked to go out of bold mode."""

    def reverse( self ) -> None:
        """Handle being asked to go to reverse mode."""

    def unreverse( self ) -> None:
        """Handle being asked to go out of reverse mode."""

    def underline( self ) -> None:
        """Handle being asked to go in underline mode."""

    def ununderline( self ) -> None:
        """Handle being asked to go out of underline mode."""

    def char( self, char: int ) -> None:
        """Handle an individual character value.

        :param int char: The character value to handle.
        """

##############################################################################
# Plain text Norton Guide line parser.
class PlainText( BaseParser ):
    """Read a line of Norton Guide text as plain text."""

    def __init__( self, line: str ) -> None:
        """Constructor.

        :param str line: The raw string to parse.
        """

        # We're going to accumulate the text into a hidden instance variable.
        self._plain = ""

        # Having set the above up, go parse.
        super().__init__( line )

    def text( self, text: str ) -> None:
        """Handle the given text.

        :param str text: The text to handle.
        """
        self._plain += text

    def char( self, char: int ) -> None:
        """Handle an individual character value.

        :param int char: The character value to handle.
        """
        self._plain += chr( char )

    def __str__( self ) -> str:
        """Return the plain text of the line.

        :returns: The parsed line, as plan text.
        :rtype: str
        """
        return self._plain

### parser.py ends here
