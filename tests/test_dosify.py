"""Library DOS-a-like utility code unit tests."""

##############################################################################
# Pytest imports.
from pytest import mark

##############################################################################
# Local imports.
from ngdb import make_dos_like


##############################################################################
@mark.parametrize(
    "source, result",
    (
        ("", ""),
        ("Hello, World!", "Hello, World!"),
        ("Ä", "─"),
    ),
)
def test_make_dos_like(source: str, result: str) -> None:
    """It can handle an empty string."""
    assert make_dos_like(source) == result


### test_dosify.py ends here
