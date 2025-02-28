"""Unit tests relating to basic guide navigation."""

##############################################################################
# Pytest imports.
from pytest import fixture, raises

##############################################################################
# Library imports.
from ngdb import NGEOF, Long, NortonGuide, Short

##############################################################################
# Local imports.
from . import BIG_GUIDE, GOOD_GUIDE


##############################################################################
@fixture
def big_guide() -> NortonGuide:
    """A guide to test with."""
    return NortonGuide(BIG_GUIDE)


##############################################################################
@fixture
def good_guide() -> NortonGuide:
    """A guide to test with."""
    return NortonGuide(GOOD_GUIDE)


##############################################################################
def test_go_first(big_guide: NortonGuide) -> None:
    """It should be possible to go to the first entry."""
    assert isinstance(big_guide.goto_first().load(), Short)


##############################################################################
def test_skip(big_guide: NortonGuide) -> None:
    """It should be possible to skip an entry without reading it."""
    assert isinstance(big_guide.goto_first().skip().load(), Long)


##############################################################################
def test_small_eof_skip(good_guide: NortonGuide) -> None:
    """A guide with one entry should EOF when skipping."""
    assert good_guide.skip().eof is True


##############################################################################
def test_small_eof_load(good_guide: NortonGuide) -> None:
    """A guide with one entry should not EOF when loading."""
    good_guide.load()
    assert good_guide.eof is False


##############################################################################
def test_big_eof_skip(big_guide: NortonGuide) -> None:
    """A guide with multiple entries should not be EOF early on during skips."""
    big_guide.goto_first()
    for _ in range(5):
        big_guide.skip()
        assert big_guide.eof is False


##############################################################################
def test_big_eof_load(big_guide: NortonGuide) -> None:
    """A guide with multiple entries should not be EOF early on during loads."""
    big_guide.goto_first()
    for _ in range(5):
        big_guide.load()
        big_guide.skip()
        assert big_guide.eof is False


##############################################################################
def test_small_eof_guard_skip(good_guide: NortonGuide) -> None:
    """Attempting to skip past the end of single-entry guide should throw an error."""
    good_guide.goto_first()
    with raises(NGEOF):
        for _ in range(100):
            good_guide.skip()


##############################################################################
def test_big_eof_guard_skip(big_guide: NortonGuide) -> None:
    """Attempting to skip past the end of multiple-entry guide should throw an error."""
    big_guide.goto_first()
    with raises(NGEOF):
        for _ in range(100):
            big_guide.skip()


##############################################################################
def test_iter_small(good_guide: NortonGuide) -> None:
    """It should be possible to iterate through a guide with one entry."""
    assert len(list(good_guide)) == 1


##############################################################################
def test_iter_big(big_guide: NortonGuide) -> None:
    """It should be possible to iterate through a guide with more than one entry."""
    assert len(list(big_guide)) == 28


### test_navigation.py ends here
