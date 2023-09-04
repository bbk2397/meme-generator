"""The interface for refactoring and imposing method implementation."""


from abc import ABC, abstractmethod
from typing import List

from .QuoteModel import QuoteModel


class IngestorInterface(ABC):
    """Can ingest any file if the text file has an allowed extension."""

    allowed_extensions = []

    @classmethod
    def can_ingest(cls, path) -> bool:
        """Test if the a given file can be ingested.

        Used to refactor code.

        :param path: the path of the file.
        """
        ext = path.split('.')[-1]
        return ext in cls.allowed_extensions

    @classmethod
    @abstractmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        """Extract quotes from a file at the given path.

        :param path: the path of the file.
        """
        pass
