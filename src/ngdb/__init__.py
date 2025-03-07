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
# Local imports.
from .dosify import make_dos_like
from .entry import Entry, Long, Short
from .guide import NortonGuide
from .link import Link
from .menu import Menu
from .parser import BaseParser, MarkupText, PlainText
from .seealso import SeeAlso
from .types import NGEOF, NGDBError, UnknownEntryType

##############################################################################
# Exports.
__all__ = (
    "BaseParser",
    "Entry",
    "Link",
    "Long",
    "make_dos_like",
    "MarkupText",
    "Menu",
    "NGDBError",
    "NGEOF",
    "NortonGuide",
    "PlainText",
    "SeeAlso",
    "Short",
    "UnknownEntryType",
)

### __init__.py ends here
