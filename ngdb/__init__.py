"""ngdb - Norton Guide database reading library."""

######################################################################
# Main library information.
__author__     = "Dave Pearson"
__copyright__  = "Copyright 2021, Dave Pearson"
__credits__    = [ "Dave Pearson" ]
__maintainer__ = "Dave Pearson"
__email__      = "davep@davep.org"
__version__    = "0.0.1"

##############################################################################
# Import things for easier access.
from .types import NGDBError, UnknownEntryType
from .guide import NortonGuide

##############################################################################
# Define what importing * means.
__all__ = (
    "NGDBError",
    "UnknownEntryType",
    "NortonGuide",
)

### __init__.py ends here
