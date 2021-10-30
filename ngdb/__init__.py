"""ngdb - Norton Guide database reading library."""

######################################################################
# Main library information.
__author__     = "Dave Pearson"
__copyright__  = "Copyright 2021, Dave Pearson"
__credits__    = [ "Dave Pearson" ]
__maintainer__ = "Dave Pearson"
__email__      = "davep@davep.org"
__version__    = "0.1.0"
__licence__    = "GPLv3+"

##############################################################################
# Import things for easier access.
from .types  import NGDBError, UnknownEntryType, NGEOF
from .guide  import NortonGuide
from .entry  import Short, Long
from .parser import BaseParser, PlainText

##############################################################################
# Define what importing * means.
__all__ = (
    "NGDBError",
    "UnknownEntryType",
    "NGEOF",
    "NortonGuide",
    "Short",
    "Long",
    "BaseParser",
    "PlainText"
)

### __init__.py ends here
