"""Test the main header reading code."""

##############################################################################
# Pytest imports.
from pytest import fixture

##############################################################################
# Library imports.
from ngdb import NortonGuide

##############################################################################
# Local imports.
from . import GOOD_GUIDE


##############################################################################
@fixture
def guide() -> NortonGuide:
    """The guide to test with."""
    return NortonGuide(GOOD_GUIDE)


##############################################################################
def test_is_ng(guide: NortonGuide) -> None:
    """It should be possible to test for a valid database."""
    assert guide.is_a is True


##############################################################################
def test_menu_count(guide: NortonGuide) -> None:
    """The menu count should read correctly."""
    assert guide.menu_count == 1


##############################################################################
def test_title(guide: NortonGuide) -> None:
    """The title should read correctly."""
    assert guide.title == "Expert Guide"


##############################################################################
def test_credits(guide: NortonGuide) -> None:
    """The credits should read correctly."""
    assert guide.credits == (
        "Expert Guide",
        "Copyright (c) 1997-2015 David A. Pearson",
        "",
        "email: davep@davep.org",
        "  web: http://www.davep.org/",
    )


##############################################################################
def test_made_with(guide: NortonGuide) -> None:
    """The test guide should be made with the Norton Guide compiler."""
    assert guide.made_with == NortonGuide.MAGIC["NG"]


### test_guide_header.py ends here
