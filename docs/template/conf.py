"""NGDB library documentation config."""

##############################################################################
# Python imports.
import os
import re
import sys

##############################################################################
# Theme module.
import sphinx_rtd_theme

##############################################################################
# Path setup.
sys.path.insert( 0, os.path.abspath( "../.." ) )

##############################################################################
# Get the library version.
from ngdb import __version__ as ngdb_version

##############################################################################
# Project information
project   = "ngdb"
copyright = "2021, Dave Pearson"
author    = "Dave Pearson"
version   = "v{}".format( re.sub( r"^(.*)\..*$", r"\1", ngdb_version ) )
release   = f"v{ngdb_version}"

##############################################################################
# General configuration.
autodoc_default_options = {
    "members": True,
    "undoc-members": True,
    "show-inheritance": True
}
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.todo",
    "sphinx.ext.intersphinx",
    "sphinx_rtd_theme"
]
templates_path    = [ "_templates" ]
source_suffix     = ".rst"
master_doc        = "index"
language          = None
exclude_patterns  = []
pygments_style    = "sphinx"
autoclass_content = "both"

##############################################################################
# Options for HTML output
html_theme           = "sphinx_rtd_theme"
html_static_path     = [ "_static" ]
html_show_sourcelink = False

##############################################################################
# Options for HTMLHelp output
htmlhelp_basename = "ngdb"

##############################################################################
# Options for todo extension
todo_include_todos = True

##############################################################################
# Link to the python docs
intersphinx_mapping = {
    "python": ( "https://docs.python.org/3.10", None )
}

### conf.py ends here
