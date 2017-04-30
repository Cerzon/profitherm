import os
from PIL import Image, ImageColor, ImageFilter
from django import template
from django.conf import settings
from django.utils.html import format_html

register = template.Library()


@register.simple_tag()
def img_thumbnail(source_path, thumb_size, tn_method='sz2fl', bg_fill='self', **kwargs):
    source_dir, source_name = os.path.split(source_path)
    if not os.path.isfile(os.path.join(settings.MEDIA_ROOT, source_path)):
        raise template.TemplateSyntaxError(
            '{} - file does not exists'.format(source_name)
        )
    width, height = (int(val) for val in thumb_size.split('x'))
    thumb_dir = os.path.join(source_dir, 'thumbnails/')
    thumb_path = os.path.join(thumb_dir, ''.join([tn_method, str(width), str(height), source_name]))
    try:
        thumb_im = Image.open(os.path.join(settings.MEDIA_ROOT, thumb_path))
    except IOError:
        try:
            source_im = Image.open(os.path.join(settings.MEDIA_ROOT, source_path))
        except IOError:
            raise template.TemplateSyntaxError(
                '{} - file can not be opened or not an image'.format(source_name)
            )
        if tn_method == 'sz2fl':
            thumb_im = do_resize_to_fill(source_im, width, height)
        else:
            thumb_im = do_resize_to_fit(source_im, width, height, bg_fill)
        if not os.path.isdir(os.path.join(settings.MEDIA_ROOT, thumb_dir)):
            os.mkdir(os.path.join(settings.MEDIA_ROOT, thumb_dir))
        try:
            thumb_im.save(os.path.join(settings.MEDIA_ROOT, thumb_path), source_im.format)
        except IOError:
            raise template.TemplateSyntaxError(
                'Unable to save thumbnail for {}'.format(source_name)
            )
        finally:
            source_im.close()
    thumb_im.close()
    return format_html('<img src="{}" {} />',
        os.path.join(settings.MEDIA_URL, thumb_path),
        ' '.join(['{}={}'.format(key, value) for key, value in kwargs.items()])
    )


def do_resize_to_fill(src_im, out_width, out_height):
    src_ratio = src_im.width / src_im.height
    output_vl = out_width / out_height
    if src_ratio > output_vl:
        output_vl = (int(out_height * src_ratio), out_height,)
    else:
        output_vl = (out_width, int(out_width / src_ratio),)
    out_im = src_im.resize(output_vl, resample=Image.BICUBIC)
    out_start_x = int((out_im.width - out_width)/2)
    out_start_y = int((out_im.height - out_height)/2)
    output_vl = (out_start_x, out_start_y, out_im.width - out_start_x, out_im.height - out_start_y)
    return out_im.crop(output_vl)


def do_resize_to_fit(src_im, out_width, out_height, background=None):
    src_ratio =  src_im.width / src_im.height
    output_vl = out_width / out_height
    if src_im.width < out_width and src_im.height < out_height:
        if background:
            out_im = src_im.copy()
        else:
            return src_im.copy()
    else:
        if src_ratio > output_vl:
            output_vl = (out_width, int(out_width / src_ratio),)
        else:
            output_vl = (int(out_height * src_ratio), out_height,)
        out_im = src_im.resize(output_vl, resample=Image.BICUBIC)
    if background:
        try:
            bg_im = ImageColor.getrgb(background)
        except ValueError:
            if isinstance(background, Image.Image):
                bg_im = background
            else:
                bg_im = src_im
            bg_im = do_resize_to_fill(bg_im, out_width, out_height)
            bg_im = bg_im.filter(ImageFilter.GaussianBlur(radius=8))
        else:
            bg_im = Image.new(src_im.mode, (out_width, out_height), bg_im)
        out_start_x = int((out_width - out_im.width)/2)
        out_start_y = int((out_height - out_im.height)/2)
        bg_im.paste(out_im, (out_start_x, out_start_y))
        out_im.close()
        return bg_im
    else:
        return out_im
