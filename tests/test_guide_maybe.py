"""Test the facility for checking if a file might be a guide."""

##############################################################################
# Python imports.
from pathlib import Path

##############################################################################
# Pytest imports.
from pytest import mark

##############################################################################
# Local imports.
from ngdb import NortonGuide


##############################################################################
@mark.parametrize(
    "candidate, expected_result",
    (
        (Path(""), False),
        (Path("ng"), False),
        (Path("ng."), False),
        (Path(".ng"), False),
        (Path(".ng.ng"), True),
        (Path("foo.txt"), False),
        (Path("foo.ng"), True),
        (Path("foo.NG"), True),
        (Path("foo.Ng"), True),
        (Path("foo.nG"), True),
        (Path("foo.bar.baz.ng"), True),
        (Path("foo.ng."), False),
        (Path("foo.ngng"), False),
        (Path("foo.ng.gz"), False),
    ),
)
def test_maybe_guide(candidate: Path, expected_result: bool) -> None:
    """We should be able to check which files might be a Norton Guide."""
    assert NortonGuide.maybe(candidate) is expected_result


### test_guide_maybe.py ends here
