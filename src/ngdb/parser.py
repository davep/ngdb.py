"""Norton Guide parser for the text inside a guide."""

##############################################################################
# Python compatibility hackage.
from __future__ import annotations

##############################################################################
# Python imports.
from abc import ABC, abstractmethod
from enum import Enum, auto
from typing import Final

##############################################################################
# Local imports.
from .dosify import make_dos_like


##############################################################################
class TextMode(Enum):
    """Types of text mode used when parsing a Norton Guide line."""

    NORMAL = auto()
    """Normal text."""
    BOLD = auto()
    """Bold text."""
    UNDERLINE = auto()
    """Underlined text."""
    REVERSE = auto()
    """Reverse text."""
    ATTR = auto()
    """Raw colour attribute."""


##############################################################################
CTRL_CHAR: Final[str] = "^"
"""The control character that marks an upcoming attribute."""


##############################################################################
class ParseState:
    """Raw text parsing state tracking class."""

    def __init__(self, line: str) -> None:
        """Constructor.

        Args:
            line: The line to work on.
        """
        self.raw = line
        """The current raw text that's left to handle."""
        self.ctrl = line.find(CTRL_CHAR)
        """The location of the next control marker."""
        self.mode = TextMode.NORMAL
        """The current mode."""
        self.last_attr = -1
        """The last attribute encountered."""

    @property
    def work_left(self) -> bool:
        """Is there any work left to do?"""
        return self.ctrl != -1 and self.ctrl < len(self.raw)

    @property
    def ctrl_id(self) -> str:
        """The current control ID."""
        try:
            return self.raw[self.ctrl + 1].lower()
        except IndexError:
            # If we've fallen in here, it's mostly because we've run into
            # some situation where there's a lone ^ at the end of the line.
            # This feels like a detail that the user-level code should not
            # be having to faff with. I feel that, as much as possible, the
            # parsing code should do its absolute best to return something
            # readable when faced with invalid markup.
            return ""


##############################################################################
class BaseParser:
    """The base text parsing class."""

    def __init__(self, line: str) -> None:
        """Constructor.

        Args:
            line: The raw string to parse.
        """

        # State tracker.
        state = ParseState(line)

        # While we've not run out of text to process...
        while state.work_left:
            # If there was text between the last markup and the next...
            if len(state.raw[: state.ctrl]) > 0:
                # ...handle it.
                self.text(state.raw[: state.ctrl])

            # Pull out the character following the control character and
            # handle it.
            if (ctrl := state.ctrl_id) == CTRL_CHAR:
                # We're looking at ^^, which is a ^.
                self.text(CTRL_CHAR)
                state.ctrl += 2
            elif hasattr(self, f"_ctrl_{ctrl}"):
                # Looks like we can handle whatever's there, so dispatch
                # it...
                getattr(self, f"_ctrl_{ctrl}")(state)
            else:
                # No idea what the next character is. We could either raise
                # an exception, eat the next character, or simply skip along
                # one. For now, let's just skip along one.
                state.ctrl += 1

            # Chop the bits we've done off the raw string.
            state.raw = state.raw[state.ctrl :]

            # Find the next control character.
            state.ctrl = state.raw.find(CTRL_CHAR)

        # Handle any remaining text.
        if len(state.raw) > 0:
            self.text(state.raw)

    def _ctrl_a(self, state: ParseState) -> None:
        """Handle ^A markup.

        Args:
            state: The data that tracks parse state.
        """

        # Get the actual attribute.
        try:
            attr = int(state.raw[state.ctrl + 2 : state.ctrl + 4], 16)
        except ValueError:
            # There wasn't a valid hex value after the ^a, so assume that
            # someone typed ^^a wrong and pretend it's a ^a.
            self.text(state.raw[state.ctrl : state.ctrl + 2])
            state.ctrl += 2
            return

        # If there's already a colour attribute in effect and the
        # new colour is the same as the previous colour...
        if state.mode is TextMode.ATTR and attr == state.last_attr:
            # ...that means it's a return to "normal".
            self.normal()
            state.mode = TextMode.NORMAL
        else:
            # ...otherwise we start a colour attribute.
            self.colour(attr)
            state.last_attr = attr
            state.mode = TextMode.ATTR

        # Skip.
        state.ctrl += 4

    def _ctrl_b(self, state: ParseState) -> None:
        """Handle ^B markup.

        Args:
            state: The data that tracks parse state.
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

    def _ctrl_c(self, state: ParseState) -> None:
        """Handle ^C markup.

        Args:
            state: The data that tracks parse state.
        """
        try:
            character = int(state.raw[state.ctrl + 2 : state.ctrl + 4], 16)
        except ValueError:
            # There wasn't a valid hex value after the ^c, so assume that
            # someone typed ^^c wrong and pretend it's a ^c.
            self.text(state.raw[state.ctrl : state.ctrl + 2])
            state.ctrl += 2
            return
        self.char(character)
        state.ctrl += 4

    def _ctrl_n(self, state: ParseState) -> None:
        """Handle ^N markup.

        Args:
            state: The data that tracks parse state.
        """
        self.normal()
        state.mode = TextMode.NORMAL
        state.ctrl += 2

    def _ctrl_r(self, state: ParseState) -> None:
        """Handle ^R markup.

        Args:
            state: The data that tracks parse state.
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

    def _ctrl_u(self, state: ParseState) -> None:
        """Handle ^U markup.

        Args:
            state: The data that tracks parse state.
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

    def text(self, text: str) -> None:
        """Handle the given text.

        Args:
            text: The text to handle.
        """
        del text  # pragma: no cover

    def colour(self, colour: int) -> None:
        """Handle the given colour value.

        Args:
            colour: The colour value to handle.
        """
        del colour  # pragma: no cover

    def normal(self) -> None:
        """Handle being asked to go to normal mode."""

    def bold(self) -> None:
        """Handle being asked to go to bold mode."""

    def unbold(self) -> None:
        """Handle being asked to go out of bold mode."""

    def reverse(self) -> None:
        """Handle being asked to go to reverse mode."""

    def unreverse(self) -> None:
        """Handle being asked to go out of reverse mode."""

    def underline(self) -> None:
        """Handle being asked to go in underline mode."""

    def ununderline(self) -> None:
        """Handle being asked to go out of underline mode."""

    def char(self, char: int) -> None:
        """Handle an individual character value.

        Args:
            char: The character value to handle.
        """
        del char  # pragma: no cover


##############################################################################
class PlainText(BaseParser):
    """Read a line of Norton Guide text as plain text."""

    def __init__(self, line: str) -> None:
        # We're going to accumulate the text into a hidden instance variable.
        self._text = ""
        # Having set the above up, go parse.
        super().__init__(line)

    def text(self, text: str) -> None:
        self._text += text

    def char(self, char: int) -> None:
        self.text(chr(char))

    def __str__(self) -> str:
        """Return the plain text of the line.

        Returns:
            The parsed line, as plan text.
        """
        return self._text


##############################################################################
class MarkupText(PlainText, ABC):
    """Read a line of Norton Guide text and mark up with start/end tags.

    This is an abstract base class for other parser classes that will
    implement start and end tags where necessary.
    """

    def __init__(self, line: str) -> None:
        # We're going to keep a stack of the markup.
        self._stack: list[str] = []
        # Having set the above up, go parse.
        super().__init__(line)

    @abstractmethod
    def open_markup(self, cls: str) -> str:
        """Open markup for the given class.

        Args:
            cls: The class of thing to open the markup for.

        Returns:
            The opening markup text.
        """
        return ""

    @abstractmethod
    def close_markup(self, cls: str) -> str:
        """Close markup for the given class.

        Args:
            cls: The class of thing to close the markup for.

        Returns:
            The closing markup text.
        """
        return ""

    def begin_markup(self, cls: str) -> None:
        """Start a section of markup.

        Args:
            cls: The class for the markup.

        Note:
            As a side-effect of calling on this, the ``close_markup`` for
            the same class will be placed on an internal stack, for use when
            ``end_markup`` is called.
        """
        self._text += self.open_markup(cls)
        self._stack.append(self.close_markup(cls))

    def end_markup(self) -> None:
        """End a section of markup."""
        self._text += self._stack.pop()

    def normal(self) -> None:
        """Handle being asked to go to normal mode.

        Note:
            Internally this also clears the whole stack of closing tags.
        """
        self._text += "".join(reversed(self._stack))
        self._stack = []

    def __str__(self) -> str:
        self.normal()
        return super().__str__()


##############################################################################
class RichText(MarkupText):
    """Read a line of Norton Guide text and mark up with Rich console markup.

    Note:
        This is implemented in a way that doesn't require that Rich is a
        dependency of this library. This is provided here as a test and a
        handy example, and one that uses [Rich's plain text BBCode-a-like
        markup](https://rich.readthedocs.io/en/stable/protocol.html).
    """

    def text(self, text: str) -> None:
        super().text(make_dos_like(text).replace("[", r"\["))

    def open_markup(self, cls: str) -> str:
        return f"[{cls}]"

    def close_markup(self, cls: str) -> str:
        del cls
        return "[/]"

    COLOUR_MAP: Final[dict[int, int]] = {
        1: 4,
        3: 6,
        4: 1,
        6: 3,
        9: 21,
        11: 14,
        12: 196,
        14: 11,
    }
    """DOS to Rich colour mapping. This is just the exceptions."""

    @classmethod
    def map_colour(cls, colour: int) -> int:
        """Map a DOS colour into a similar colour from Rich.

        Args:
            colour: The DOS colour to map from.

        Returns:
            The mapped colour.
        """
        return cls.COLOUR_MAP.get(colour, colour)

    def colour(self, colour: int) -> None:
        self.begin_markup(
            f"color({self.map_colour(colour & 0xF)}) on color({self.map_colour(colour >> 4 & 0xF)})"
        )

    def bold(self) -> None:
        self.begin_markup("bold")

    def unbold(self) -> None:
        self.end_markup()

    def reverse(self) -> None:
        self.begin_markup("reverse")

    def unreverse(self) -> None:
        self.end_markup()

    def underline(self) -> None:
        self.begin_markup("underline")

    def ununderline(self) -> None:
        self.end_markup()


### parser.py ends here
