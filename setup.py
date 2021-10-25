"""Setup file for the NGDB library."""

##############################################################################
# Imports.
from pathlib    import Path
from setuptools import setup, find_packages

##############################################################################
# Import the library itself to pull details out of it.
import ngdb

##############################################################################
# Work out the location of the README file.
def readme():
    """Return the full path to the README file.

    :returns: The path to the README file.
    :rtype: ~pathlib.Path
    """
    return Path( __file__).parent.resolve() / "README.md"

##############################################################################
# Load the long description for the package.
def long_desc():
    """Load the long description of the package from the README.

    :returns: The long description.
    :rtype: str
    """
    with readme().open( "r", encoding="utf-8" ) as rtfm:
        return rtfm.read()

##############################################################################
# Perform the setup.
setup(

    name                          = "ngdb",
    version                       = ngdb.__version__,
    description                   = ngdb.__doc__,
    long_description              = long_desc(),
    long_description_content_type = "text/markdown",
    url                           = "https://github.com/davep/ngdb.py",
    author                        = ngdb.__author__,
    author_email                  = ngdb.__email__,
    maintainer                    = ngdb.__maintainer__,
    maintainer_email              = ngdb.__email__,
    packages                      = find_packages(),
    package_data                  = { "ngdb": [ "py.typed" ] },
    include_package_data          = True,
    python_requires               = ">=3.8",
    keywords                      = "library dbase clipper norton guide reader",
    classifiers                   = (
        "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
        "Development Status :: 3 - Alpha",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Documentation",
        "Topic :: Software Development :: Documentation",
        "Topic :: Software Development :: Libraries",
        "Typing :: Typed"
    )

)

### setup.py ends here
