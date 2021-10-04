"""Base Norton Guide interaction unit tests."""

##############################################################################
# Python imports.
from unittest import TestCase

##############################################################################
# Library imports.
from ngdb import NortonGuide

##############################################################################
# Local imports.
from . import GOOD_GUIDE, MISSING_GUIDE

##############################################################################
# Test various forms of opening a guide.
class TestOpen( TestCase ):
    """Norton Guide opening tests."""

    def test_open_good( self ) -> None:
        """It should be possible to open a good guide that exists."""
        guide = NortonGuide( GOOD_GUIDE )
        self.assertTrue( guide.is_open )
        guide.close()

    def test_open_missing_guide( self ) -> None:
        """Opening a missing guide show throw the correct exception."""
        with self.assertRaises( FileNotFoundError ):
            _ = NortonGuide( MISSING_GUIDE )

### test_guide_base.py ends here
