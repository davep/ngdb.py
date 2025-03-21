"""Test the code that handles expanding run-length-encoded spaces."""

##############################################################################
# Pytest imports.
from pytest import mark

##############################################################################
# Local imports.
from ngdb.reader import GuideReader


##############################################################################
@mark.parametrize(
    "compressed, expanded",
    [
        ("", ""),
        (" ", " "),
        ("\xff\x00", ""),
        ("\xff\x01", " "),
        ("\xff\x0a", " " * 10),
        ("\xff\xff", " "),
        ("\xff", " "),
        ("X\xff\x00", "X"),
        ("X\xff\x01", "X "),
        ("X\xff\x0a", "X" + (" " * 10)),
        ("X\xff\xff", "X "),
        ("X\xff", "X "),
        ("\xff\x00X", "X"),
        ("\xff\x01X", " X"),
        ("\xff\x0aX", (" " * 10) + "X"),
        ("\xff\xffX", " X"),
        ("X\xff\x00X", "XX"),
        ("X\xff\x01X", "X X"),
        ("X\xff\x0aX", "X" + (" " * 10) + "X"),
        ("X\xff\xffX", "X X"),
    ],
)
def test_unrle(compressed: str, expanded: str) -> None:
    """The code to expand run-length-encoded spaces should work."""
    assert GuideReader.unrle(compressed) == expanded


### test_unrle.py ends here
