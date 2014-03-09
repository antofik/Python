# coding=utf-8
import datetime
from django.http import HttpResponse, Http404, HttpResponseBadRequest
from django.template import RequestContext
from django.shortcuts import render_to_response, redirect
import logging
import string
from django.utils.log import logger
from models import Photo, Tournament
from forms import DressForm
import random
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.core.files.uploadedfile import UploadedFile
from django.utils import simplejson
from sorl.thumbnail import get_thumbnail

log = logging.getLogger('default')
new_dress_key = 'new_dress_id'
code_key = 'access'    

def home(request):
    dresses = Tournament.objects.filter(confirmed=True)
    return render_to_response('home.html', {'dresses':dresses}, context_instance=RequestContext(request))
    
def dress_view(request, id):
    try:
        log.info('dress_view')
        photos = Photo.objects.filter(tournament_id=id)
        log.info('photos = %s, count = %s' % (photos, len(photos)))
        try:
            dress = Tournament.objects.get(pk=id)
            log.info('dress = %s' % dress)
        except Exception, e:
            log.info('error in tournament = %s' % str(e))
            raise Http404
        return render_to_response('dress.html', {'photos':photos, 'dress':dress}, context_instance=RequestContext(request))
    except Exception, e:
        log.error(str(e))
        return HttpResponse("Error")
    
@csrf_exempt    
def dress_new(request):
    if request.method=='POST':
        try:
            id = int(request.session[new_dress_key])
            dress = Tournament.objects.get(pk=id)
        except:
            raise Http404
        form = DressForm(count=len(request.FILES), data=request.POST, files=request.FILES)
        if form.is_valid():
            dress = form.save(request.FILES, dress)
            request.session[new_dress_key] = None
            return redirect(dress)
        else:
            form.save_photos(dress)
    else:    
        if new_dress_key in request.session.keys():                        
            try:
                id = int(request.session[new_dress_key])
                dress = Tournament.objects.get(pk=id)
                if not dress.confirmed:
                    dress.delete()
            except:
                pass
    
        dress = Tournament()
        dress.confirmed = False
        dress.date = datetime.datetime.now()
        dress.access_key = ''.join(random.choice(string.letters) for i in xrange(DressForm.ACCESS_KEY_LENGTH))
        dress.save()

        request.session[new_dress_key] = dress.id
        
        form = DressForm()
        
        if settings.DEBUG:
            form.load_test_data()
    return render_to_response('dress_edit.html', {'form':form, 'is_new':True, 'dress': dress}, context_instance=RequestContext(request))
   
def dress_edit(request, id):
    try:
        id = int(id)
    except:
        raise Http404

    if (not request.session.get(code_key)) or (id not in request.session.get(code_key)):
        return redirect('/login/%s' % id)        
      
    try:
        dress = Tournament.objects.select_related('photo_set').get(pk=id)
    except:
        raise Http404
    
    if request.method=='POST':
        form = DressForm(count=len(request.FILES), data=request.POST, files=request.FILES)
        if form.is_valid():
            dress = form.save(request.FILES, dress)
            return redirect(dress)
        else:
            form.save_photos(dress)
    else:
        form = DressForm()
        form.load_data(dress)

    return render_to_response('dress_edit.html', {'form':form, 'dress':dress, 'is_new':False}, context_instance=RequestContext(request))

@csrf_exempt    
def load_photo(request):
    if request.method=='POST':
        if request.FILES is None:
            return HttpResponseBadRequest('No file[] found')

        try:
            id = int(request.POST['id'])
            tournament = Tournament.objects.get(pk=id)
            if tournament is None:
                return HttpResponseBadRequest('Cannot find corresponding dress')
        except:
            return HttpResponseBadRequest('Cannot find id')            
            
        file = request.FILES[u'files[]']
        
        if str(file).lower()[-4:] not in ['.jpg', 'jpeg', '.gif', '.png', '.bmp', '.ico',]:
            return HttpResponseBadRequest('Only images allowed')
        
        wrapped_file = UploadedFile(file)
        filename = wrapped_file.name
        file_size = wrapped_file.file.size
    
        photo = Photo()        
        photo.tournament = tournament
        photo.description = filename
        photo.image = file
        photo.save()

        try:
            im = get_thumbnail(photo.image, "200", quality=50)
            thumb_url = im.url
        except Exception, ex:
            photo.delete()
            return HttpResponseBadRequest('Cannot read thumbnail')   
    
        result = [{"name": filename,
                   "id": photo.id,
                   "size": file_size,
                   "url": photo.image.url,
                   "thumbnail_url": thumb_url,
                   }]
        response_data = simplejson.dumps(result)

        mimetype = 'text/plain'
        if 'HTTP_ACCEPT_ENCODING' in request.META.keys():
            if "application/json" in request.META['HTTP_ACCEPT_ENCODING']:
                mimetype = 'application/json'
        return HttpResponse(response_data, mimetype=mimetype)
    else:
        raise Http404
