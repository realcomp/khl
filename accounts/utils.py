# coding: utf-8
import operator

from django.core.files.uploadedfile import InMemoryUploadedFile

from StringIO import StringIO
from PIL import Image


def make_avatar(data, name, size):
    '''
    Resize image

    data: image data
    size: tuple(width, height)
    '''
    image = Image.open(data)
    # compare aspect ratio
    if operator.div(*map(float, size)) > operator.div(*map(float, image.size)):
        new_size = size[0], 1000
    else:
        new_size = 1000, size[1]
    image.thumbnail(new_size, Image.ANTIALIAS)
    # thumbnail = Image.new('RGBA', size, (255, 255, 255, 0))
    # thumbnail.paste(image, (
    #     int((size[0] - image.size[0]) / 2),
    #     int((size[1] - image.size[1]) / 2)))
    buf = StringIO()
    # thumbnail.save(buf, format='jpeg')
    image.save(buf, format='jpeg')
    return InMemoryUploadedFile(buf, 'image', name, None, buf.tell(), None)
