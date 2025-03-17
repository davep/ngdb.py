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
    ],
)
def test_unrle(compressed: str, expanded: str) -> None:
    """The code to expand run-length-encoded spaces should work."""
    assert GuideReader.unrle(compressed) == expanded


### test_unrle.py ends here
