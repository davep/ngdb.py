"""Provides a class that is the base for a prompt collection."""

##############################################################################
# Python imports.
from typing import Tuple, Iterator, Final, NamedTuple

##############################################################################
# Single prompt data.
class Prompt( NamedTuple ):
    """Named tuple that holds the data for a single prompt."""

    #: The text of the prompt.
    prompt: str
    #: The offset of the prompt.
    offset: int

##############################################################################
# Base class for classes that are collections of prompts and offsets.
class PromptCollection:
    """Base class for classes that contain prompt/offset collections."""

    #: The maximum length of a prompt in a guide.
    MAX_PROMPT_LENGTH: Final = 128

    def __init__( self ) -> None:
        """Constructor."""
        self._count                      = 0
        self._prompts: Tuple[ str, ... ] = ()
        self._offsets: Tuple[ int, ... ] = ()

    @property
    def prompts( self ) -> Tuple[ str, ... ]:
        """The prompts in the collection.

        :type: Tuple[str,...]
        """
        return self._prompts

    @property
    def offsets( self ) -> Tuple[ int, ... ]:
        """The offsets into the guide for each prompt.

        :type: Tuple[int,...]
        """
        return self._offsets

    def __len__( self ) -> int:
        """Get the number of prompts in the collection.

        :returns: The count of prompts.
        :rtype: int
        """
        return self._count

    def __getitem__( self, prompt: int ) -> Prompt:
        """Get a prompt/offset pair.

        :returns: The requested prompt and its offset.
        :rtype: Prompt
        """
        return Prompt( self.prompts[ prompt ], self.offsets[ prompt ] )

    def __iter__( self ) -> Iterator[ Prompt ]:
        """Get an iterator of prompt and offset pairs.

        :yields: Prompt
        """
        return ( Prompt( *prompt ) for prompt in zip( self.prompts, self.offsets ) )

    def __bool__( self ) -> bool:
        """Test if there are any prompts in the collection.

        :returns: ``True`` if there are prompts, ``False`` if not.
        :rtype: bool
        """
        return bool( len( self ) )

### prompts.py ends here
