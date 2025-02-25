"""Display information about Norton Guide files."""

##############################################################################
# Python imports.
import argparse
from pathlib import Path

##############################################################################
# Local imports.
from .. import NortonGuide, __version__


##############################################################################
def get_args() -> argparse.Namespace:
    """Get the arguments passed by the user.

    Returns:
        argparse.Namespace: The parsed arguments.
    """

    # Version information, used in a couple of paces.
    version = f"v{__version__}"

    # Create the argument parser object.
    parser = argparse.ArgumentParser(
        description="Display information about a Norton Guide Database file",
        epilog=version,
    )

    # Add --version
    parser.add_argument(
        "-v",
        "--version",
        help="Show version information.",
        action="version",
        version=f"%(prog)s {version}",
    )

    # The remainder is the path to the guides to look at.
    parser.add_argument(
        "guides", nargs="+", help="The guides to get information for", type=Path
    )

    # Parse the command line.
    return parser.parse_args()


##############################################################################
def info(guide_path: Path, verbose: bool = False) -> None:
    """Dump Norton Guide information to stdout.

    Args:
        guide_path (Path): The path to the guide to print info for.
        verbose (bool, optional): Flag to say if verbose information should be printed.

    Note:
        If not provided, ``verbose`` defaults to ``False``.
    """
    with NortonGuide(guide_path) as guide:
        print(
            f"{guide.magic:2} {guide_path.stem:20} "
            f"{guide.title if guide.is_a else '- Not a Norton Guide Database -'}"
        )
        if verbose:
            print("\n")
            print("\n".join(guide.credits))


##############################################################################
def main() -> None:
    """Main function."""
    for guide in (args := get_args()).guides:
        info(guide, verbose=(len(args.guides) == 1))


##############################################################################
# Main entry point.
if __name__ == "__main__":
    main()

### nginfo.py ends here
