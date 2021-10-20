"""Norton Guide parser for the text inside a guide."""

##############################################################################
# Python imports.
from enum import Enum, auto

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
# Base parser class.
class BaseParser:
    """The base text parsing class."""

    #: The control character that marks an upcoming attribute.
    CTRL_CHAR = "^"

    def __init__( self, raw: str ) -> None:
        """Constructor.

        :param str raw: The raw string to parse.
        """

        ctrl      = raw.index( self.CTRL_CHAR )
        mode      = TextMode.NORMAL
        last_attr = -1

        # While we've not run out of text to process...
        while ctrl != -1 and ctrl < len( raw ):

            # Handle the text we have.
            self.text( raw[ :ctrl ] )

            # Pull out the character following the control character.
            this = raw[ ctrl + 1 ].upper

            # Colour attribute?
            if this == "A":

                # Get the actual attribute.
                attr = int( raw[ ctrl+2:ctrl+4 ], 16 )

                # If there's already a colour attribute in effect and the
                # new colour is the same as the previous colour...
                if mode is TextMode.ATTR and attr == last_attr:
                    # ...that means it's a return to "normal".
                    this.normal()
                    mode = TextMode.NORMAL
                else:
                    # ...otherwise we start a colour attribute.
                    this.colour( last_attr := attr )
                    mode = TextMode.ATTR

                # Bump along.
                ctrl += 4

            elif this == "B":

                # If we're in bold mode...
                if mode is TextMode.BOLD:
                    # ...go back to normal.
                    self.unbold()
                    mode = TextMode.NORMAL
                else:
                    # ...otherwise go bold!
                    self.bold()
                    mode = TextMode.BOLD

                # Skip!
                ctrl += 2

            elif this == "C":
                self.char( int( raw[ ctrl+2:ctrl+4 ], 16 ) )
                ctrl += 4

            elif this == "N":
                self.normal()
                mode = TextMode.NORMAL
                ctrl += 2

            elif this == "R":

                # If we're in reverse mode...
                if mode is TextMode.REVERSE:
                    # ...go back to normal.
                    self.unreverse()
                    mode = TextMode.NORMAL
                else:
                    # ...otherwise go reverse.
                    self.reverse()
                    mode = TextMode.REVERSE

                # Skip!
                ctrl += 2

            elif this == "U":

                # If we're in underline mode...
                if mode is TextMode.UNDERLINE:
                    # ...go back to normal.
                    self.ununderline()
                    mode = TextMode.NORMAL
                else:
                    # ...otherwise go underline.
                    self.underline()
                    mode = TextMode.UNDERLINE

                # Skip!
                ctrl += 2

            elif this == self.CTRL_CHAR:
                self.text( self.CTRL_CHAR )
                ctrl += 2

            else:
                ctrl += 1

            # Chop the bits we've done off the raw string.
            raw = raw[ ctrl: ]

            # Find the next control character.
            ctrl = raw.index( self.CTRL_CHAR )

        # Handle any remaining text.
        self.text( raw )

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
