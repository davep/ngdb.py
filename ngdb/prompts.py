"""Provides a class that is the base for a prompt collection."""

##############################################################################
# Python compatibility hackage.
from __future__ import annotations

##############################################################################
# Python imports.
from typing import Final, Iterator

##############################################################################
# Local imports.
from .link import Link


##############################################################################
class PromptCollection:
    """Base class for classes that contain prompt/offset collections."""

    MAX_PROMPT_LENGTH: Final[int] = 128
    """The maximum length of a prompt in a guide."""

    def __init__(self) -> None:
        """Constructor."""
        self._count = 0
        self._prompts: tuple[str, ...] = ()
        self._offsets: tuple[int, ...] = ()

    @property
    def prompts(self) -> tuple[str, ...]:
        """The prompts in the collection."""
        return self._prompts

    @property
    def offsets(self) -> tuple[int, ...]:
        """The offsets into the guide for each prompt."""
        return self._offsets

    def __len__(self) -> int:
        """Get the number of prompts in the collection.

        Returns:
            The count of prompts.
        """
        return self._count

    def __getitem__(self, prompt: int) -> Link:
        """Get a prompt/offset pair.

        Returns:
            The requested prompt and its offset.
        """
        return Link(self.prompts[prompt], self.offsets[prompt])

    def __iter__(self) -> Iterator[Link]:
        """Get an iterator of prompt and offset pairs.

        Yields:
            A link containing the prompt/offset, from the collection.
        """
        return (Link(*prompt) for prompt in zip(self.prompts, self.offsets))

    def __bool__(self) -> bool:
        """Test if there are any prompts in the collection.

        Returns:
            ``True`` if there are prompts, ``False`` if not.
        """
        return bool(len(self))


### prompts.py ends here
