"""Test the main header reading code."""

##############################################################################
# Python imports.
from unittest import TestCase

##############################################################################
# Library imports.
from ngdb import NortonGuide

##############################################################################
# Local imports.
from . import GOOD_GUIDE

##############################################################################
# Test various attributes of a Norton Guide database header.
class TestHeader( TestCase ):
    """Norton Guide database header tests."""

    def test_is_ng( self ) -> None:
        """It should be possible to test for a valid database."""
        self.assertTrue( NortonGuide( GOOD_GUIDE ).is_a )

### test_guide_header.py ends here
