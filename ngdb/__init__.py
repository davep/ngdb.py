"""ngdb - Norton Guide database reading library."""

######################################################################
# Main library information.
__author__     = "Dave Pearson"
__copyright__  = "Copyright 2021-2022, Dave Pearson"
__credits__    = [ "Dave Pearson" ]
__maintainer__ = "Dave Pearson"
__email__      = "davep@davep.org"
__version__    = "0.5.0"
__licence__    = "GPLv3+"

##############################################################################
# Import things for easier access.
from .types  import NGDBError, UnknownEntryType, NGEOF
from .guide  import NortonGuide
from .entry  import Entry, Short, Long
from .parser import BaseParser, PlainText
from .dosify import make_dos_like

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
    "make_dos_like"
)

### __init__.py ends here
