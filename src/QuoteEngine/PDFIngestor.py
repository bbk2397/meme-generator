"""The pdf ingestor used to ingest quotes from pdf files."""


from typing import List
import subprocess
from subprocess import PIPE
import os

from .IngestorInterface import IngestorInterface
from .QuoteModel import QuoteModel
from .TextFileQuoteParser import TextFileQuoteParser


class PDFIngestor(IngestorInterface, TextFileQuoteParser):
    """Can parse pdf files if the file has an allowed extension."""

    allowed_extensions = ['pdf']

    @classmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        """Extract quotes from a file at the given path.

        :param path: the path of the file.
        """
        if not cls.can_ingest(path):
            raise Exception('cannot ingest exception')

        tmp = 'tmp__pdf_text'
        subprocess.run(['pdftotext', path, tmp])
        quotes = cls.parse_text_file(tmp)
        os.remove(tmp)

        return quotes
