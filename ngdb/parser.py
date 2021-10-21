"""Norton Guide parser for the text inside a guide."""

##############################################################################
# Python imports.
from enum        import Enum, auto
from dataclasses import dataclass

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
# Class to help track the state of raw parsing.
@dataclass
class ParseTracker:
    """Raw text parsing state tracking class."""

    #: The location of the next control character.
    ctrl: int

    #: The raw string we're working with.
    raw: str

    #: The current text mode.
    mode: TextMode = TextMode.NORMAL

    #: The last encountered attribute.
    last_attr: int = -1

##############################################################################
# Base parser class.
class BaseParser:
    """The base text parsing class."""

    #: The control character that marks an upcoming attribute.
    CTRL_CHAR = "^"

    def __init__( self, line: str ) -> None:
        """Constructor.

        :param str line: The raw string to parse.
        """

        track = ParseTracker( line.index( self.CTRL_CHAR ), line )

        # While we've not run out of text to process...
        while track.ctrl != -1 and track.ctrl < len( track.raw ):

            # Handle the text we have.
            self.text( track.raw[ :track.ctrl ] )

            # Pull out the character following the control character.
            this = track.raw[ track.ctrl + 1 ].upper

            # Colour attribute?
            if this == "A":
                self._ctrl_a( track )

            elif this == "B":
                self._ctrl_b( track )

            elif this == "C":
                self._ctrl_c( track )

            elif this == "N":
                self._ctrl_n( track )

            elif this == "R":
                self._ctrl_r( track )

            elif this == "U":
                self._ctrl_u( track )

            elif this == self.CTRL_CHAR:
                self.text( self.CTRL_CHAR )
                track.ctrl += 2

            else:
                track.ctrl += 1

            # Chop the bits we've done off the raw string.
            track.raw = track.raw[ track.ctrl: ]

            # Find the next control character.
            track.ctrl = track.raw.index( self.CTRL_CHAR )

        # Handle any remaining text.
        self.text( track.raw )

    def _ctrl_a( self, track: ParseTracker ) -> None:
        """Handle ^A markup.

        :param ParseTracker track: The data that tracks parse state.
        """

        # Get the actual attribute.
        attr = int( track.raw[ track.ctrl+2:track.ctrl+4 ], 16 )

        # If there's already a colour attribute in effect and the
        # new colour is the same as the previous colour...
        if track.mode is TextMode.ATTR and track.attr == track.last_attr:
            # ...that means it's a return to "normal".
            self.normal()
            track.mode = TextMode.NORMAL
        else:
            # ...otherwise we start a colour attribute.
            self.colour( attr )
            track.last_attr = attr
            track.mode      = TextMode.ATTR

        # Skip.
        track.ctrl += 4

    def _ctrl_b( self, track: ParseTracker ) -> None:
        """Handle ^B markup.

        :param ParseTracker track: The data that tracks parse state.
        """

        # If we're in bold mode...
        if track.mode is TextMode.BOLD:
            # ...go back to normal.
            self.unbold()
            track.mode = TextMode.NORMAL
        else:
            # ...otherwise go bold!
            self.bold()
            track.mode = TextMode.BOLD

        # Skip!
        track.ctrl += 2

    def _ctrl_c( self, track: ParseTracker ) -> None:
        """Handle ^C markup.

        :param ParseTracker track: The data that tracks parse state.
        """
        self.char( int( track.raw[ track.ctrl+2:track.ctrl+4 ], 16 ) )
        track.ctrl += 4

    def _ctrl_n( self, track: ParseTracker ) -> None:
        """Handle ^N markup.

        :param ParseTracker track: The data that tracks parse state.
        """
        self.normal()
        track.mode = TextMode.NORMAL
        track.ctrl += 2

    def _ctrl_r( self, track: ParseTracker ) -> None:
        """Handle ^R markup.

        :param ParseTracker track: The data that tracks parse state.
        """

        # If we're in reverse mode...
        if track.mode is TextMode.REVERSE:
            # ...go back to normal.
            self.unreverse()
            track.mode = TextMode.NORMAL
        else:
            # ...otherwise go reverse.
            self.reverse()
            track.mode = TextMode.REVERSE

        # Skip!
        track.ctrl += 2

    def _ctrl_u( self, track: ParseTracker ) -> None:
        """Handle ^U markup.

        :param ParseTracker track: The data that tracks parse state.
        """

        # If we're in underline mode...
        if track.mode is TextMode.UNDERLINE:
            # ...go back to normal.
            self.ununderline()
            track.mode = TextMode.NORMAL
        else:
            # ...otherwise go underline.
            self.underline()
            track.mode = TextMode.UNDERLINE

        # Skip!
        track.ctrl += 2

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

    def char( self, char_val: int ) -> None:
        """Handle an individual character value."""

### parser.py ends here
