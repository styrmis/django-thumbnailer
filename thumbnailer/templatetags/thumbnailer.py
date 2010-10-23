from django.template import Library
from django.core.urlresolvers import reverse
from django.conf import settings

register = Library()

# TODO:
# 1) Set /thumb/ in settings for both urls.py and here

@register.filter
def thumbnail(image, size):
    width, height = size.split('x')
    
    width  = width != '' and int(width) or None
    height = height != '' and int(height) or None
    
    qargs = []
    if width != None: qargs.append("width=%d" % width)
    if height != None: qargs.append("height=%d" % height)
    qstring = '&'.join(qargs)
    
    url = "%s%s?%s" % ( '/thumb/', image.name, qstring )
    
    return url
