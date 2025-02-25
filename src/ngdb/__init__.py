"""ngdb - Norton Guide database reading library."""

##############################################################################
# Python imports.
from importlib.metadata import version

######################################################################
# Main library information.
__author__ = "Dave Pearson"
__copyright__ = "Copyright 2021-2025, Dave Pearson"
__credits__ = ["Dave Pearson"]
__maintainer__ = "Dave Pearson"
__email__ = "davep@davep.org"
__version__ = version("ngdb")
__licence__ = "GPLv3+"

##############################################################################
# Import things for easier access.
from .dosify import make_dos_like
from .entry import Entry, Long, Short
from .guide import NortonGuide
from .parser import BaseParser, MarkupText, PlainText
from .types import NGEOF, NGDBError, UnknownEntryType

##############################################################################
# Define what importing * means.
__all__ = (
    "NGDBError",
    "UnknownEntryType",
    "NGEOF",
    "NortonGuide",
    "Entry",
    "Short",
    "Long",
    "BaseParser",
    "PlainText",
    "MarkupText",
    "make_dos_like",
)

### __init__.py ends here
