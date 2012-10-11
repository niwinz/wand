# -*- coding: utf-8 -*-

from .api import library
from .image import Image


class Sequence(object):
    """
    MagickWand's image sequences manager.

    :param image: An `Image` instance
    :type image: :class:`Image`
    """

    def __init__(self, image, clone_on_access=True):
        """
        Constructor. Only accept images with sequences.
        By default, on access on subimage, always creata a clone, but this
        uses a mount of memory. If you want to preserve the memory,
        you can disable this behavior with ``clone_by_default`` parameter.
        """

        if not isinstance(image, Image):
            raise TypeError('expected a wand.image.Image instance, '
                            'not ' + repr(image))

        if not image.has_sequence():
            raise ValueError("Current image does not have secuence.")

        self.image = image.clone()
        self.clone = clone_on_access

    def __del__(self):
        self.image.destroy()

    def __len__(self):
        return library.MagickGetNumberImages(self.image.wand)

    def __getitem__(self, index):
        """
        List access method. Usefull for access
        to all images on a sequence like a native python list.

        Example::

            image = Image(filename="someimage.pdf")
            seq = Sequence(image)
            seq[2].save(filename="image2.png")

        """

        if not 0 <= index < len(self):
            raise ValueError('value could be between 0 and %s' % len(self))

        if self.clone:
            image = self.image.clone()
        else:
            image = self.image

        library.MagickSetIteratorIndex(image.wand, index)
        return image

    def get_current_index(self):
        """
        Get current secuence index.
        """
        return library.MagickGetIteratorIndex(self.image.wand)

    def append(self, image):
        """
        Append image to the end of sequence.
        """
        self.insert(len(self) - 1, image)

    def insert(self, index, image):
        """
        Insert image in concrete position.
        """
        if not isinstance(image, Image):
            raise TypeError('expected a wand.image.Image instance, '
                            'not ' + repr(image))

        if not 0 <= index < len(self):
            raise ValueError('value could be between 0 and %s' % len(self))

        current_index = self.get_current_index()
        library.MagickSetIteratorIndex(self.image.wand, index)
        library.MagickAddImage(self.image.wand, image.wand)
        library.MagickSetIteratorIndex(self.image.wand, current_index)
