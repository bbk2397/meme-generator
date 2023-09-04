"""Parse a text file in order to find all quotes."""


from typing import List

from .QuoteModel import QuoteModel
from .NoQuoteException import NoQuoteException
from .StrQuoteParser import StrQuoteParser


class TextFileQuoteParser(StrQuoteParser):
    """Can extract all quotes from a file."""

    @classmethod
    def parse_text_file(cls, path: str) -> List[QuoteModel]:
        """Extract quotes from a text file at the given path.

        :param path: the path of the file.
        """
        quotes = []
        with open(path) as fh:
            for line in fh:
                try:
                    quotes.append(cls.parse_quote(line))
                except NoQuoteException:
                    continue

        return quotes
