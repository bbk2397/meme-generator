"""The model for a quote."""


class QuoteModel():
    """Initialize and represent a quote."""

    def __init__(self, body, author):
        """Initialize the quote.

        :param body: the body of the quote.
        :param author: the author of the quote.
        """
        self.body = body
        self.author = author

    def __repr__(self):
        """Represent the quote in a way quotes are usually represented."""
        return f'"{self.body}" - {self.author}'
