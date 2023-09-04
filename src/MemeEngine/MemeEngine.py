"""A module to create memes."""


from PIL import Image, ImageFont, ImageDraw
import os
from pathlib import Path


class MemeEngine():
    """Initialize the engine and create memes."""

    _input_image_extensions = ['jpg', 'jpeg', 'png']

    def __init__(self, output_dir: str = './tmp'):
        """Initialize the engine with the path to save the image to.

        :param output_dir: the path the manipulated image will be saved to.
        """
        self.output_dir = output_dir
        try:
            os.mkdir(self.output_dir)
        except FileExistsError:
            print('Info: the directory already exists.')

    def make_meme(self, img_path, text, author, width=500) -> str:
        """Place a quote on an image.

        As precondition, one has to provide a path of an image that exists.

        The quote has a text and an author.
        Returns the path to the manipulated image.

        It will try to avoid overwriting an already processed image.

        :param img_path: the image that will have the quote
        :text (str): the body of the quote
        :author (str): the author of the quote
        """
        if not Path(img_path).is_file():
            raise Exception('file does not exist')

        lowered = img_path.lower()
        is_right_file = False
        for extension in MemeEngine._input_image_extensions:
            if lowered.endswith(extension):
                is_right_file = True
                break

        if not is_right_file:
            raise Exception('file extension not supported')

        img = Image.open(img_path)

        if width is not None:
            ratio = width/float(img.size[0])
            height = int(ratio*float(img.size[1]))
            img = img.resize((width, height), Image.NEAREST)

        if text is not None:
            body = f'"{text}"'

            draw_text = ImageDraw.Draw(img).text

            MemeEngine._draw_text(draw_text, body, 24)
            if author is not None:
                author = f'- {author}'
                MemeEngine._draw_text(draw_text, author, 14, x=40, y=60)

        file_name = self._get_file_name(img_path)

        count = 1
        while True:
            processed_file_name = f'processed__{count}__{file_name}'
            path = Path(f'{self.output_dir}/{processed_file_name}')
            if not path.is_file():
                break
            count += 1

        img.save(path)
        return path

    def _get_file_name(self, img_path: str) -> str:
        """Return a file name that wasn't used until now.

        Hint: this can be used to avoid writing over the file.

        :param img_path: the path of the image given as input.
        """
        if img_path is None:
            raise Exception('the path of the input image is required')

        file_name = ''
        for ch in img_path[::-1]:
            if ch == '/' or ch == '\\':
                break
            file_name += ch

        return file_name[::-1]

    @classmethod
    def _draw_text(cls,
                   draw_text,
                   text, font_size,
                   x=10,
                   y=30,
                   border='white',
                   font_color='black'):
        """Draw text with border.

        :param draw_text: the method used to draw text. It has to be what
        returns ImageDraw.Draw(img).text
        :param text: the text to be drawn that will have border
        :param font_size: the size of the font
        :param x: the x component of the position of the text on the image
        :param y: the y component of the position of the text on the image
        :param border: the color of the drawn text's border
        :param font_color: the color of the font of the drawn text
        """
        font = ImageFont.truetype('arial.ttf', size=font_size)
        offset = 1
        draw_text((x-offset, y), text, font=font, fill=border)
        draw_text((x+offset, y), text, font=font, fill=border)
        draw_text((x, y-offset), text, font=font, fill=border)
        draw_text((x, y+offset), text, font=font, fill=border)

        draw_text((x, y), text, font=font, fill=font_color)
