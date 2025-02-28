"""Norton Guide entry tests."""

##############################################################################
# Pytest imports.
from pytest import fixture, raises

##############################################################################
# Library imports.
from ngdb import Entry, Long, NortonGuide, Short, UnknownEntryType
from ngdb.types import EntryType

##############################################################################
# Local imports.
from . import BIG_GUIDE


##############################################################################
@fixture
def guide() -> NortonGuide:
    """The guide to test with."""
    return NortonGuide(BIG_GUIDE)


##############################################################################
@fixture
def short(guide: NortonGuide) -> Short:
    """A short guide entry to test against."""
    assert isinstance(entry := guide.goto_first().load(), Short)
    return entry


##############################################################################
@fixture
def long(guide: NortonGuide) -> Long:
    """A long guide entry to test against."""
    assert isinstance(entry := guide.goto_first().skip().load(), Long)
    return entry


##############################################################################
def test_unknown(guide: NortonGuide) -> None:
    """Attempting to load an unknown entry type should result in an exception."""
    with raises(UnknownEntryType):
        guide.goto(0).load()


##############################################################################
def test_short_load_correct_type(short: Entry) -> None:
    """A short entry should load as the correct type."""
    assert isinstance(short, Short)


##############################################################################
def test_short_correct_id(short: Entry) -> None:
    """A short entry should have a short entry ID."""
    assert short.type_id == 0
    assert EntryType.is_short(short.type_id) is True
    assert EntryType.is_long(short.type_id) is False


##############################################################################
def test_short_entry_size(short: Entry) -> None:
    """The test short entry should have the correct size."""
    assert short.size == 838


##############################################################################
def test_short_parent(short: Entry) -> None:
    """The test short entry should not have a parent."""
    assert bool(short.parent) is False


##############################################################################
def test_short_parent_line(short: Entry) -> None:
    """It test should entry should not have a parent line."""
    assert short.parent.has_line is False


##############################################################################
def test_short_parent_menu(short: Entry) -> None:
    """The test short entry should have a parent menu."""
    assert short.parent.has_menu is True


##############################################################################
def test_short_parent_prompt(short: Entry) -> None:
    """The test short entry should have a parent menu prompt."""
    assert short.parent.has_prompt is True


##############################################################################
def test_short_previous(short: Entry) -> None:
    """The test short should not have a previous entry."""
    assert short.has_previous is False


##############################################################################
def test_short_next(short: Entry) -> None:
    """The test short should not have a next entry."""
    assert short.has_next is False


##############################################################################
def test_short_str_entry(short: Entry) -> None:
    """The str() of the short entry should be the main text."""
    assert len(str(short).split("\n")) == len(short)


##############################################################################
def test_short_lines_and_offsets(short: Short) -> None:
    """There should be equal numbers of lines and offsets for the short."""
    assert len(short.lines) == len(short.offsets)


##############################################################################
def test_short_list_like(short: Short) -> None:
    """It should be possible to treat a short entry like a list."""
    assert short[0] == (
        " OL_95AppTitle()          Set/get the Windows 95 application title.",
        1389,
    )
    assert (
        short[0].text
        == " OL_95AppTitle()          Set/get the Windows 95 application title."
    )
    assert short[0].offset == 1389
    assert short[0].has_offset is True


##############################################################################
def test_iter_iter(short: Short) -> None:
    """It should be possible to treat a short entry like an iterator."""
    assert next(iter(short)) == (
        " OL_95AppTitle()          Set/get the Windows 95 application title.",
        1389,
    )


##############################################################################
def test_long_load_correct_type(long: Long) -> None:
    """A long entry should load as the correct type."""
    assert isinstance(long, Long)


##############################################################################
def test_long_correct_id(long: Long) -> None:
    """A long entry should have a long entry ID."""
    assert long.type_id == 1
    assert EntryType.is_short(long.type_id) is False
    assert EntryType.is_long(long.type_id) is True


##############################################################################
def test_long_entry_size(long: Long) -> None:
    """The long entry should have the correct size."""
    assert long.size == 940


##############################################################################
def test_long_parent(long: Long) -> None:
    """The long entry should have a parent."""
    assert bool(long.parent) is True


##############################################################################
def test_long_parent_line(long: Long) -> None:
    """The long entry should have a parent line."""
    assert long.parent.has_line is True
    assert long.parent.line == 0


##############################################################################
def test_long_parent_menu(long: Long) -> None:
    """The test long entry should have a parent menu."""
    assert long.parent.has_menu is True


##############################################################################
def test_long_parent_prompt(long: Long) -> None:
    """The test long entry should have a parent menu prompt."""
    assert long.parent.has_prompt is True


##############################################################################
def test_long_previous(long: Long) -> None:
    """The test long entry should not have a previous entry."""
    assert long.has_previous is False


##############################################################################
def test_long_next(long: Long) -> None:
    """The test long entry should have a next entry."""
    assert long.has_next is True


##############################################################################
def test_long_str_entry(long: Long) -> None:
    """The str() of the test long entry should be the main text."""
    assert len((str_entry := str(long)).split("\n")) == len(long)


##############################################################################
def test_long_list_like(long: Long) -> None:
    """It should be possible to treat a long entry like a list."""
    assert long[0] == " ^bOL_95AppTitle()"


##############################################################################
def test_long_iter_like(long: Long) -> None:
    """It should be possible to treat a long entry like an iterator."""
    assert next(iter(long)) == " ^bOL_95AppTitle()"


##############################################################################
def test_long_see_also(long: Long) -> None:
    """The test long entry should have a see-also menu."""
    assert bool(long.see_also)


##############################################################################
def test_long_see_also_count(long: Long) -> None:
    """The test long entry should have the correct number of see-also items."""
    assert len(long.see_also) == 1


##############################################################################
def test_long_see_also_text(long: Long) -> None:
    """The test long entry should have the correct see-also prompt."""
    assert long.see_also.prompts[0] == "OL_95VMTitle()"


##############################################################################
def test_long_see_also_offset(long: Long) -> None:
    """The test long entry should have the correct see-also offset."""
    assert long.see_also.offsets[0] == 2355


##############################################################################
def test_long_see_also_list_like(long: Long) -> None:
    """It should be possible to treat the see-also object like a list."""
    assert long.see_also[0] == ("OL_95VMTitle()", 2355)


##############################################################################
def test_long_see_also_iter_like(long: Long) -> None:
    """It should be possible to treat the see-also object like an iterator."""
    assert next(iter(long.see_also)) == ("OL_95VMTitle()", 2355)


### test_guide_entry.py ends here
