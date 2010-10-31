from django.http import HttpResponseRedirect
from django.conf import settings

from cuddlybuddly.thumbnail.main import Thumbnail

def produce_thumbnail_and_redirect(request, path):
    width   = request.GET.has_key('width') and int(request.GET['width']) or None
    height  = request.GET.has_key('height') and int(request.GET['height']) or None
    
    if width is not None or height is not None:
        thumb = Thumbnail(path, width, height)
        dest_path = thumb.final_dest
    else:
        dest_path = path
    
    return HttpResponseRedirect(settings.MEDIA_URL + dest_path)
