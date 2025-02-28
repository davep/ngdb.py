"""Guide menu unit tests."""

##############################################################################
# Pytest imports.
from pytest import fixture

##############################################################################
# Library imports.
from ngdb import NortonGuide
from ngdb.menu import Menu

##############################################################################
# Local imports.
from . import BIG_GUIDE


##############################################################################
@fixture
def guide() -> NortonGuide:
    """The guide to test with."""
    return NortonGuide(BIG_GUIDE)


##############################################################################
def test_has_menus(guide: NortonGuide) -> None:
    """The test guide has the correct number of menus."""
    assert guide.menu_count == 1
    assert guide.menu_count == len(guide.menus)
    assert all(isinstance(menu, Menu) for menu in guide.menus)


##############################################################################
def test_menu_title(guide: NortonGuide) -> None:
    """The menu title should load correctly."""
    assert guide.menus[0].title == "OSLIB"
    assert guide.menus[0].title == str(guide.menus[0])


##############################################################################
def test_menu_options(guide: NortonGuide) -> None:
    """The menu options should load correctly."""
    assert guide.menus[0].prompts == (
        "Functions",
        "FAQs",
        "Revision History",
        "Credits",
        "About",
    )
    assert [prompt.text for prompt in guide.menus[0]] == [
        "Functions",
        "FAQs",
        "Revision History",
        "Credits",
        "About",
    ]


##############################################################################
def test_menu_item(guide: NortonGuide) -> None:
    """It should be possible to treat a menu like a list."""
    assert guide.menus[0][0][0] == "Functions"
    assert guide.menus[0][0].text == "Functions"
    assert str(guide.menus[0][0]) == "Functions"
    assert guide.menus[0][0][1] == 525
    assert guide.menus[0][0].offset == 525
    assert int(guide.menus[0][0]) == 525
    assert guide.menus[0][0]


### test_guide_menu.py ends here
