# coding: utf-8
from django import template
from django.template.context import *
from django.utils.safestring import mark_safe
from pyqrcode import MakeQRImage
from cStringIO import StringIO
import base64

register = template.Library()

@register.simple_tag
def qr_code(string):
    image = MakeQRImage(string,block_in_pixels = 2)
    png = StringIO()
    image.save(png,"PNG")
    content = base64.b64encode(png.getvalue()).replace('\n', '')
    return '<img style="vertical-align:middle;" src="data:image/png;base64,%s" />' % content
