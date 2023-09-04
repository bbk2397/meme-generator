"""The text ingestor used to ingest quotes from text files."""

from typing import List

from .IngestorInterface import IngestorInterface
from .QuoteModel import QuoteModel
from .TextFileQuoteParser import TextFileQuoteParser


class TextIngestor(IngestorInterface, TextFileQuoteParser):
    """Can parse text files if the file has an allowed extension."""

    allowed_extensions = ['txt']

    @classmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        """Extract quotes from a file at the given path.

        :param path: the path of the file.
        """
        if not cls.can_ingest(path):
            raise Exception('cannot ingest exception')

        return cls.parse_text_file(path)
