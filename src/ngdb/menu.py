"""Code for loading and holding guide menus."""

##############################################################################
# Local imports.
from .prompts import PromptCollection
from .reader import GuideReader


##############################################################################
class Menu(PromptCollection):
    """Class that loads and holds the details of a menu in the guide."""

    def __init__(self, guide: GuideReader) -> None:
        """Constructor.

        Args:
            guide: The reader object for the guide.
        """

        # Call the parent first.
        super().__init__()

        # Skip the type marker for the menu. Our caller should have tested
        # that we're a menu.
        _ = guide.read_word(False)

        # Skip the byte size of the menu section.
        _ = guide.read_word(False)

        # Next up, read the prompt count.
        self._count = guide.read_word() - 1

        # Now skip 20 bytes. I'm not sure what they are.
        guide.skip(20)

        # Next up is the collection of offsets for each menu prompt.
        self._offsets = tuple(guide.read_offset() for _ in range(len(self)))

        # Skip a number of values I don't know the purpose of, but I've
        # never needed. It seems to be two sets of long integer arrays.
        guide.skip((len(self) + 1) * 8)

        # We've now got to the title of the menu.
        self._title = guide.unrle(guide.read_strz(self.MAX_PROMPT_LENGTH))

        # After the title comes the prompts.
        self._prompts = tuple(
            guide.unrle(guide.read_strz(self.MAX_PROMPT_LENGTH))
            for _ in range(len(self))
        )

        # Finally, skip an unknown byte. This should then place us on the
        # next "record" in the database.
        guide.skip()

    @property
    def title(self) -> str:
        """The title of the menu."""
        return self._title

    def __str__(self) -> str:
        """Get the string representation of the menu.

        Returns:
            The title of the menu.
        """
        return self.title

    def __repr__(self) -> str:
        """Get the string representation of the menu.

        Returns:
            The title of the menu.
        """
        return f"<{self.__class__.__name__}: {self}>"


### menu.py ends here
