"""Code for loading and holding guide menus."""

##############################################################################
# Python imports.
from typing import Tuple, Iterator

##############################################################################
# Local imports.
from .reader import GuideReader

##############################################################################
# Menu class.
class Menu:
    """Class that loads and holds the details of a menu in the guide."""

    #: The maximum length of a prompt in a guide.
    MAX_PROMPT_LENGTH = 128

    def __init__( self, guide: GuideReader ) -> None:
        """Constructor.

        :param GuideReader guide: The reader object for the guide.
        """

        # Skip the type marker for the menu. Our caller should have tested
        # that we're a menu.
        _ = guide.read_word( False )

        # Skip the byte size of the menu section.
        _ = guide.read_word( False )

        # Next up, read the prompt count.
        self._prompt_count = guide.read_word() - 1

        # Now skip 20 bytes. I'm not sure what they are.
        guide.skip( 20 )

        # Next up is the collection of offsets for each menu prompt.
        self._offsets = tuple( guide.read_long() for _ in range( len( self ) ) )

        # Skip a number of values I don't know the purpose of, but I've
        # never needed. It seems to be two sets of long integer arrays.
        guide.skip( ( len( self ) + 1 ) * 8 )

        # We've now got to the title of the menu.
        self._title = guide.read_strz( self.MAX_PROMPT_LENGTH )

        # After the title comes the prompts.
        self._prompts = tuple(
            guide.read_strz( self.MAX_PROMPT_LENGTH ) for _ in range( len( self ) )
        )

        # Finally, skip an unknown byte. This should then place us on the
        # next "record" in the database.
        guide.skip()

    def __len__( self ) -> int:
        """The count of prompts in the menu."""
        return self._prompt_count

    def __getitem__( self, prompt: int ) -> Tuple[ str, int ]:
        """Get a menu item's information."""
        return self.prompts[ prompt ], self.offsets[ prompt ]

    @property
    def title( self ) -> str:
        """The title of the menu.

        :type: str
        """
        return self._title

    @property
    def prompts( self ) -> Tuple[ str, ... ]:
        """The prompts in the menu.

        :type: Tuple[str,...]
        """
        return self._prompts

    @property
    def offsets( self ) -> Tuple[ int, ... ]:
        """The offsets into the guide for each prompt.

        :type: Tuple[int,...]
        """
        return self._offsets

    def __iter__( self ) -> Iterator[ Tuple[ str, int ] ]:
        """Get an iterator of prompt and offset pairs."""
        return ( ( prompt, offset ) for prompt, offset in zip( self.prompts, self.offsets ) )

    def __repr__( self ) -> str:
        """The string representation of the menu."""
        return f"<{self.__class__.__name__}: {self.title}>"

### menu.py ends here
