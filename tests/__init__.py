"""ngdb unit tests."""

##############################################################################
# Python imports.
from pathlib import Path

##############################################################################
# Test database names.
GUIDES_BASE = Path(__name__).resolve() / "guides"
GOOD_GUIDE = GUIDES_BASE / "eg.ng"
BIG_GUIDE = GUIDES_BASE / "oslib.ng"
MISSING_GUIDE = GUIDES_BASE / "does-not-exist.ng"

### __init__.py ends here
