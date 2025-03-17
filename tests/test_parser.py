"""Norton Guide entry content markup unit tests."""

##############################################################################
# Python compatibility hackage.
from __future__ import annotations

##############################################################################
# Python imports.
from typing import Iterator

##############################################################################
# Backward compatibility.
from typing_extensions import TypeAlias

##############################################################################
# Library imports.
from ngdb import BaseParser, PlainText
from ngdb.parser import RichText


##############################################################################
class TestPlainText:
    """Perform parser tests against the plain text parser."""

    def test_empty_string(self) -> None:
        """It can handle an empty line."""
        assert str(PlainText("")) == ""

    def test_no_markup(self) -> None:
        """It can handle a line with no markup."""
        assert str(PlainText("Test")) == "Test"

    def test_strips_non_text_markup(self) -> None:
        """It should strip all non-text markup without issue."""
        assert (
            str(PlainText("^A10This ^Bis ^Na ^Rtest, ^Ureally it is."))
            == "This is a test, really it is."
        )

    def test_strips_only_non_text_markup(self) -> None:
        """It should turn non-text markup only into an empty string."""
        assert str(PlainText("^A10^B^N^R^U")) == ""

    def test_ctrl_ctrl(self) -> None:
        """^^ should become ^."""
        assert str(PlainText("^^" * 10)) == ("^" * 10)

    def test_char_code(self) -> None:
        """It should be able to handle character codes."""
        assert str(PlainText("^C20^C21")) == " !"

    def test_truncated_markup(self) -> None:
        """It should handle truncated markup."""
        assert str(PlainText("^")) == ""


##############################################################################
TEvent: TypeAlias = str | tuple[str, str | int]
"""Type of a single event that the TestParser will catch."""

##############################################################################
TEvents: TypeAlias = list[TEvent]
"""Type of the collection of events in the TestParser."""


##############################################################################
# Unit-test-oriented Norton Guide line parser.
class MockedParser(BaseParser):
    """Parser class for working with unit tests."""

    def __init__(self, line: str) -> None:
        # First off, we're going to collect all the different events that
        # happen, so start a list for doing that.
        self._events: TEvents = []

        # Then call the super.
        super().__init__(line)

    def text(self, text: str) -> None:
        self._events.append(("T", text))

    def colour(self, colour: int) -> None:
        self._events.append(("A", colour))

    def normal(self) -> None:
        self._events.append("N")

    def bold(self) -> None:
        self._events.append("B")

    def unbold(self) -> None:
        self._events.append("b")

    def reverse(self) -> None:
        self._events.append("R")

    def unreverse(self) -> None:
        self._events.append("r")

    def underline(self) -> None:
        self._events.append("U")

    def ununderline(self) -> None:
        self._events.append("u")

    def char(self, char: int) -> None:
        self._events.append(("C", char))

    def __iter__(self) -> Iterator[TEvent]:
        """The collection of events caught by the parser."""
        return iter(self._events)


##############################################################################
class TestParseEvents:
    """Test the various events that happen within a parser."""

    def test_empty_line(self) -> None:
        """There should be no events in an empty line."""
        assert list(MockedParser("")) == []

    def test_no_markup(self) -> None:
        """There should be a single text event for a non-markup line."""
        assert list(MockedParser("Hello, World!")) == [("T", "Hello, World!")]

    def test_colour(self) -> None:
        """There should be a colour event when there's a ^A."""
        assert list(MockedParser("Hello, ^A20World!")) == [
            ("T", "Hello, "),
            ("A", 0x20),
            ("T", "World!"),
        ]

    def test_multi_colour(self) -> None:
        """Multiple there should be multiple colour events with multiple ^A."""
        assert list(MockedParser("Hello, ^A20World^A64!")) == [
            ("T", "Hello, "),
            ("A", 0x20),
            ("T", "World"),
            ("A", 0x64),
            ("T", "!"),
        ]

    def test_same_colour(self) -> None:
        """Two consecutive ^A of the same colour should cause a ^N."""
        assert list(MockedParser("Hello, ^A20World^A20!")) == [
            ("T", "Hello, "),
            ("A", 0x20),
            ("T", "World"),
            "N",
            ("T", "!"),
        ]

    def test_bold(self) -> None:
        """It should be possible to turn bold on and off with ^B."""
        assert list(MockedParser("Hello, ^BWorld^B!")) == [
            ("T", "Hello, "),
            "B",
            ("T", "World"),
            "b",
            ("T", "!"),
        ]

    def test_char(self) -> None:
        """It should be possible to generate characters with ^C."""
        assert list(MockedParser("".join(f"^C{n:02x}" for n in range(256)))) == [
            ("C", n) for n in range(256)
        ]

    def test_normal(self) -> None:
        """A ^N markup should result in a back-to-normal event."""
        assert list(MockedParser("Hello, ^NWorld!")) == [
            ("T", "Hello, "),
            "N",
            ("T", "World!"),
        ]

    def test_reverse(self) -> None:
        """It should be possible to turn reverse on and off with ^R."""
        assert list(MockedParser("Hello, ^RWorld^R!")) == [
            ("T", "Hello, "),
            "R",
            ("T", "World"),
            "r",
            ("T", "!"),
        ]

    def test_underline(self) -> None:
        """It should be possible to turn underline on and off with ^U."""
        assert list(MockedParser("Hello, ^UWorld^U!")) == [
            ("T", "Hello, "),
            "U",
            ("T", "World"),
            "u",
            ("T", "!"),
        ]


##############################################################################
class TestParseBadSource:
    """Test various examples of bad guide source I've encountered."""

    def test_unescaped_ctrl_a(self) -> None:
        """A ^a that doesn't seem to be followed by numbers should be treated as a ^a."""
        assert list(MockedParser("This is a ^a that ^aisn't escaped correctly")) == [
            ("T", "This is a "),
            ("T", "^a"),
            ("T", " that "),
            ("T", "^a"),
            ("T", "isn't escaped correctly"),
        ]

    def test_unescaped_ctrl_c(self) -> None:
        """A ^c that doesn't seem to be followed by numbers should be treated as a ^c."""
        assert list(MockedParser("This is a ^c that ^cisn't escaped correctly")) == [
            ("T", "This is a "),
            ("T", "^c"),
            ("T", " that "),
            ("T", "^c"),
            ("T", "isn't escaped correctly"),
        ]


##############################################################################
class TestRichParser:
    """Test the Rich-friendly parser."""

    def test_empty_line(self) -> None:
        """An empty line should parse fine."""
        assert str(RichText("")) == ""

    def test_no_markup(self) -> None:
        """A line with no markup should parse fine."""
        assert str(RichText("Hello, World!")) == "Hello, World!"

    def test_escape_markup(self) -> None:
        """Text that looks like Rich markup should get escaped."""
        assert str(RichText("Hello, [W]orld!")) == "Hello, \\[W]orld!"

    def test_colour(self) -> None:
        """A colour attribute should come out as the expected markup."""
        assert str(RichText("^A02Hello")) == "[color(2) on color(0)]Hello[/]"

    def test_bold(self) -> None:
        """A bold attribute should turn into the Rich version."""
        assert str(RichText("^BHello^b")) == "[bold]Hello[/]"

    def test_reverse(self) -> None:
        """A reverse attribute should turn into the Rich version."""
        assert str(RichText("^RHello^r")) == "[reverse]Hello[/]"

    def test_underline(self) -> None:
        """An underline attribute should turn into the Rich version."""
        assert str(RichText("^UHello^u")) == "[underline]Hello[/]"


### test_parser.py ends here
