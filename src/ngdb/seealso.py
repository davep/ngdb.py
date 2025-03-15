"""See-also loading/holding code."""

##############################################################################
# Python imports.
from typing import Final

##############################################################################
# Local imports.
from .prompts import PromptCollection
from .reader import GuideReader


##############################################################################
class SeeAlso(PromptCollection):
    """Class to load and hold all the see alsos for a long entry."""

    MAX_SEE_ALSO: Final[int] = 20
    """Max number of see also items we'll handle.

    This is the limit published in the Expert Help Compiler manual and,
    while this limit isn't really needed in this code, it does help guard
    against corrupt guides.
    """

    def __init__(self, guide: GuideReader, load: bool) -> None:
        """Constructor.

        Args:
            guide: The reader object for the guide.
            load: Should we bother trying to load any?

        Note:
            The `load` parameter might look a bit daft, and it is, but a
            Norton Guide has a flag to say if there are any see-also entries
            *and* a count value later on, which won't be there and won't be
            0 if the flag is 0. So... we pass the flag in here and just have
            a see-also collection that has nothing in it.

            I could, of course, make the use of this class optional but that
            feels icky.
        """

        # Call the parent first.
        super().__init__()

        # Should we actually bother trying to load anything?
        if load:
            # Get the count of see-also entries.
            self._count = min(guide.read_word(), self.MAX_SEE_ALSO)

            # Get the offsets for each of the see-also entries.
            self._offsets = tuple(guide.read_offset() for _ in range(len(self)))

            # Get the prompts for each of the see-also items.
            self._prompts = tuple(
                guide.unrle(guide.read_strz(self.MAX_PROMPT_LENGTH))
                for _ in range(len(self))
            )


### seealso.py ends here
