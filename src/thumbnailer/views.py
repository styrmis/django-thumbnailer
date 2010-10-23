from django.shortcuts import render_to_response
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.conf import settings

from cultlabs.cuddlybuddly.thumbnail.main import Thumbnail

import urllib2, mimetypes, md5, os
from StringIO import StringIO
from urlparse import urlparse, urlunparse
from PIL import Image

from django.core.files.storage import default_storage

THUMBS_DIR = '/tmp/thumbs'
DEFAULT_QUALITY = 92

def produce_thumbnail(request):
    url     = request.GET['url']
    width   = request.GET.has_key('width') and int(request.GET['width']) or None
    height  = request.GET.has_key('height') and int(request.GET['height']) or None
    quality = request.GET.has_key('quality') and int(request.GET['quality']) or None
    
    rq_hash = md5.new(url).hexdigest()
    parsed = urlparse(url)
    image_url = urlunparse((parsed.scheme, parsed.netloc, parsed.path, '', '', ''))
    mimetype = mimetypes.guess_type(image_url)[0]
    
    if width or height or quality:        
        try:
            contents = StringIO(urllib2.urlopen(image_url).read())
            
            image = Image.open(contents)
            
            orig_width, orig_height = image.size
            orig_ratio = float(orig_width) / float(orig_height)
            
            tn_width = int( ((width != None) and float(width)) or float(height)*ratio )
            tn_height = int( ((height != None) and float(height)) or float(width)/ratio )
            
            tn_path = os.path.join(THUMBS_DIR, rq_hash)
            
            if not os.path.exists(tn_path):
                # If tn doesn't exist, resize and save
                image.thumbnail([tn_width, tn_height], Image.ANTIALIAS)
                
                if image.format == 'gif':
                    image.save(tn_path, image.format, dither=Image.NONE, palette=Image.ADAPTIVE, quality=DEFAULT_QUALITY)
                else:
                    image.save(tn_path, image.format, quality=DEFAULT_QUALITY)
            
            tn_file = open(tn_path, 'rb')
            
            return HttpResponse(tn_file, mimetype=mimetype)
        except urllib2.HTTPError:
            raise Http404, '"%s" does not exist' % image_url
    else:
        # No parameters so just return the image as is.
        try:
            contents = urllib2.urlopen(image_url).read()
            
            response = HttpResponse(contents, mimetype=mimetype)
            response["Content-Length"] = len(contents)
            return response
        except urllib2.HTTPError:
            raise Http404, '"%s" does not exist' % image_url

def produce_thumbnail_and_redirect(request, path):
    width   = request.GET.has_key('width') and int(request.GET['width']) or None
    height  = request.GET.has_key('height') and int(request.GET['height']) or None
    
    if width is not None or height is not None:
        thumb = Thumbnail(path, width, height)
        dest_path = thumb.dest
    else:
        dest_path = path
    
    return HttpResponseRedirect(settings.MEDIA_URL + dest_path)
    