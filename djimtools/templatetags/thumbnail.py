import os
from PIL import Image
from django import template
from django.conf import settings

register = template.Library()


@register.simple_tag()
def img_thumbnail(source_path, thumb_size, **kwargs):
    source_dir, source_name = os.path.split(source_path)
    source_fullpath = os.path.join(settings.MEDIA_ROOT, source_path)
    width, height = thumb_size.split('x')
    width = int(width)
    height = int(height)
    thumb_name = ''.join(['tn', str(width), str(height), source_name])
    thumb_path = os.path.join(source_dir, 'thumbnails/', thumb_name)
    try:
        thumb_im = Image.open(os.path.join(settings.MEDIA_ROOT, thumb_path))
    except IOError:
        try:
            source_im = Image.open(source_fullpath)
        except IOError:
            if not os.path.isfile(source_fullpath):
                exc_msg = '{} - file does not exists'.format(source_name)
            else:
                exc_msg = '{} - file can not be opened or not an image'.format(source_name)
            raise template.TemplateSyntaxError(exc_msg)
        #thumb_ratio = width/height
        #source_ratio = source_im.width/source_im.height
        #if source_ratio > thumb_ratio:
        #    r_size = (int(height*source_ratio), height)
        #else:
        #    r_size = (width, int(width/source_ratio))
        #thumb_im = source_im.resize(r_size, Image.BICUBIC)
        thumb_im = source_im.copy()
        source_im.close()
        thumb_im.thumbnail((width, height))
        try:
            thumb_im.save(os.path.join(settings.MEDIA_ROOT, thumb_path), 'jpeg')
        except IOError:
            raise template.TemplateSyntaxError(
                'Unable to save thumbnail for {}'.format(source_name)
            )
        return '<img src="{0}" {1}>'.format(thumb_path, ' '.join(['{}="{}"'.format(key, value) for key, value in kwargs.items()]))
