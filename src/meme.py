"""Meme generator that uses general quote ingestors and meme generator."""


import os
import random
import argparse

from QuoteEngine import Ingestor, QuoteModel
from MemeEngine import MemeEngine


def generate_meme(path=None, body=None, author=None):
    """Generate a meme given an path and a quote."""
    img = None
    quote = None

    if path is None:
        images = "./_data/photos/dog/"
        imgs = []
        for root, dirs, files in os.walk(images):
            imgs = [os.path.join(root, name) for name in files
            if not name == '.directory']

        img = random.choice(imgs)
    else:
        img = path

    if body is None:
        quote_files = ['./_data/DogQuotes/DogQuotesTXT.txt',
                       './_data/DogQuotes/DogQuotesDOCX.docx',
                       './_data/DogQuotes/DogQuotesPDF.pdf',
                       './_data/DogQuotes/DogQuotesCSV.csv']
        quotes = []
        for f in quote_files:
            quotes.extend(Ingestor.parse(f))

        quote = random.choice(quotes)
    else:
        if author is None:
            raise Exception('Author Required if Body is Used')
        quote = QuoteModel(body, author)

    meme = MemeEngine('./tmp')
    path = meme.make_meme(img, quote.body, quote.author)
    return path


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="""Returns path to a
        generated meme.""")
    parser.add_argument('--path', type=str, help="""What is the path to
        the image on which you want to have a quote on?""")
    parser.add_argument('--body', type=str, help="""What is the body of
        the quote to add to the image?""")
    parser.add_argument('--author', type=str, help="""Who is the author
        of the given body quote to add to the image?""")

    args = parser.parse_args()
    print(generate_meme(args.path, args.body, args.author))
