"""Base Norton Guide interaction unit tests."""

##############################################################################
# Pytest imports.
from pytest import raises

##############################################################################
# Library imports.
from ngdb import NortonGuide

##############################################################################
# Local imports.
from . import GOOD_GUIDE, MISSING_GUIDE


##############################################################################
def test_open_good() -> None:
    """It should be possible to open a good guide that exists."""
    with NortonGuide(GOOD_GUIDE) as guide:
        assert guide.is_open


##############################################################################
def test_open_missing_guide() -> None:
    """Opening a missing guide show throw the correct exception."""
    with raises(FileNotFoundError):
        _ = NortonGuide(MISSING_GUIDE)


##############################################################################
def test_with_closes_guide() -> None:
    """When `with` is used with a guide, it should be closed afterwards.."""
    with NortonGuide(GOOD_GUIDE) as guide:
        assert guide.is_open is True
    assert guide.is_open is False


##############################################################################
def test_str() -> None:
    """The str() of the object should be the path to the file."""
    assert str(NortonGuide(GOOD_GUIDE)) == str(GOOD_GUIDE)


### test_guide_base.py ends here
