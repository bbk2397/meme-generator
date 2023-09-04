"""The docx ingestor used to ingest quotes from docx files."""

from typing import List
import docx

from .IngestorInterface import IngestorInterface
from .QuoteModel import QuoteModel
from .StrQuoteParser import StrQuoteParser
from .NoQuoteException import NoQuoteException


class DocxIngestor(IngestorInterface, StrQuoteParser):
    """Can parse docx files if the file has an allowed extension."""

    allowed_extensions = ['docx']

    @classmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        """Extract quotes from a file at the given path.

        :param path: the path of the file.
        """
        if not cls.can_ingest(path):
            raise Exception('cannot ingest exception')

        quotes = []
        doc = docx.Document(path)
        for p in doc.paragraphs:
            try:
                quotes.append(cls.parse_quote(p.text))
            except NoQuoteException:
                continue

        return quotes
