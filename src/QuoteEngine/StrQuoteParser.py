"""Parse a text in order to find a quote."""


from .QuoteModel import QuoteModel
from .NoQuoteException import NoQuoteException


class StrQuoteParser():
    """Parses a quote from a line of text."""

    @classmethod
    def parse_quote(cls, line: str) -> QuoteModel:
        """Parse a quote in a given line of text.

        :param line: str: the line of text to be parsed
        """
        line = line.rstrip()
        if len(line) <= 0:
            raise NoQuoteException('The given line does not have a quote')
        body_to_author = line.split(' - ')
        body = body_to_author[0].strip('"')
        author = body_to_author[1]
        return QuoteModel(body, author)
