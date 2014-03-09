# coding=utf-8
from datetime import datetime
from django.contrib.auth.decorators import permission_required
from django.http import HttpResponse, Http404, HttpResponseBadRequest
from django.template import RequestContext
from django.shortcuts import render_to_response, redirect
import logging
import string
from models import Photo, Dress, Reply
from forms import DressForm, LoginForm
import random
from django.conf import settings
from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_exempt
from django.core.files.uploadedfile import UploadedFile
from django.utils import simplejson
from django.contrib.sites.models import Site
from sorl.thumbnail import get_thumbnail

log = logging.getLogger('default')
new_dress_key = 'new_dress_id'
code_key = 'access'    


def home(request):    
    dresses = Dress.objects.filter(blocked=False).filter(confirmed=True).filter(sold=False).filter(complains__lte=5)
    types = Photo.GALLERY_CHOICES
    vk_share_url = 'catalog.mfst.pro'
    types = [x[0] for x in Dress.DRESS_TYPES]
    categories = [x[0] for x in Dress.DANCER_CATEGORY]
    return render_to_response('home.html', {'dresses':dresses, 'types':types, 'categories':categories, 'vk_share_url':vk_share_url}, context_instance=RequestContext(request))
    
def dress_view(request, id):    
    photos = Photo.objects.filter(dress_id=id)
    try:
        dress = Dress.objects.get(pk=id)
    except:
        raise Http404
    
    rating = dress.rating.get_rating_for_user(request.user, ip_address=request.META['REMOTE_ADDR'], cookies=request.COOKIES)
    if rating is None:
        rating = False

        
    photos = photos
   
    if not dress.views:
        dress.show_hint=True
    record_view(request, dress)       

    vk_share_url = 'catalog.mfst.pro/dress/%s' % id
    return render_to_response('dress.html', {'photos':photos, 'rating': rating, 'dress':dress, 'vk_share_url':vk_share_url}, context_instance=RequestContext(request))
    
@csrf_exempt    
def dress_new(request):
    if request.method=='POST':
        try:
            id = int(request.session[new_dress_key])
            dress = Dress.objects.get(pk=id)
        except: 
            raise Http404
        form = DressForm(count=len(request.FILES), data=request.POST, files=request.FILES)        
        if form.is_valid():
            dress = form.save(request.FILES, dress, send_email=True)
            request.session[new_dress_key] = None
            return redirect(dress)
        else:
            form.save_photos(dress)
    else:    
        if new_dress_key in request.session.keys():                        
            try:
                id = int(request.session[new_dress_key])
                dress = Dress.objects.get(pk=id)
                if not dress.confirmed:
                    dress.delete()
            except: 
                pass
    
        dress = Dress()
        dress.confirmed = False
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
        dress = Dress.objects.select_related('photo_set').get(pk=id)
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
            dress = Dress.objects.get(pk=id)
            if dress is None:
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
        photo.dress = dress
        photo.description = filename
        photo.image = file
        photo.gallery = Photo.GALLERY_CHOICES[0][0]
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
     
def login(request, id):
    try:
        id = int(id)
    except:
        raise Http404

    if not request.session.get(code_key):
        request.session[code_key] = []
        
    error = None
        
    if request.method=='POST':
        form = LoginForm(request.POST)
        if form.is_valid():    
            if form.save(id):
                request.session[code_key].append(id)
                return redirect('/dress/edit/%s' % id)            
            else:
                error = u'Неправильный код доступа'
    else:
        form = LoginForm()
    
    return render_to_response('login.html', {'form':form, 'id':id, 'error': error}, context_instance=RequestContext(request))
    
def record_view(request, dress):
    key = 'viewed'
    if key not in request.session.keys():
        request.session[key] = []
    if dress.id not in request.session[key]:
        request.session[key].append(dress.id)
        dress.views += 1
        dress.save()

def remind_access_code(request, id):
    if request.method != 'POST':
        log.error('[remind_access_code] method != POST: %s' % request.method)
        raise Http404

    ok = True
    invalid_email = False

    try:
        id = int(id)
        email = request.POST['email']
        dress = Dress.objects.get(pk=id)
        if dress.email != email:
            print('----------------', dress.email, '----------------')
            invalid_email = True
            ok = False
    except:
        dress = None
        ok = False

        #============== Email template ================    
        #TODO: move email template to separate file
    message = u'''
Добрый день

    Вы запросили напоминание кода доступа к вашему обявлению о продаже платья.
    Ваш код доступа: {access_key}
    Вы всегда можете просмотреть и изменить ваше объявление по ссылке http://catalog.mfst.pro/dress/{dressid}

    С уважением, 
        Команда mfst.pro'''
        #==============================================

    if ok:
        message = message.format(dressid=dress.id, access_key=dress.access_key)
        send_mail('[catalog.mfst.pro] Напоминание кода доступа', message, 'no-reply@mfst.pro', [dress.email], fail_silently=False)

    result = {"ok": ok,"invalid_email":invalid_email}
    response_data = simplejson.dumps(result)

    mimetype = 'text/plain'
    if 'HTTP_ACCEPT_ENCODING' in request.META.keys():
        if "application/json" in request.META['HTTP_ACCEPT_ENCODING']:
            mimetype = 'application/json'
    return HttpResponse(response_data, mimetype=mimetype)

def send_notification(request):
    if request.method != 'POST':
        log.error('[send_notification] method != POST: %s' % request.method)
        raise Http404
        
    try:
        id = int(request.POST['id'])
        fio = request.POST['fio']
        email = request.POST['email']
        phone = request.POST['phone']

        dress = Dress.objects.get(pk=id)
    except Exception, ex:
        log.error('[send_notification] %s' % ex)
        raise Http404

    #============== Email template ================
    #TODO: move email template to separate file
    message = u'''

Ваше платье хотят примерить!

    Имя: {fio}
    Телефон: {phone}
    Email: {email}
    Дата оставления заявки: {date}

    Просмотреть анкету можно по ссылке http://{site}{dress_url}
    Там же вы найдёте общий список желаюжщих примерить ваше платье.
    
Внимание! Это автоматическое письмо, не отвечайте на него.

    С уважением, 
        Команда mfst.pro'''
        #==============================================

    try:
        current_site = Site.objects.get_current()
        domain = current_site.domain
        message = message.format(site=domain, dress_url=dress.get_absolute_url(), fio=fio, email=email, phone=phone, date=datetime.now())

        print "Dress", dress
        print "DressId", dress.id

        reply = Reply()
        reply.dress = dress
        reply.date = datetime.now()
        reply.fio = fio
        reply.email = email
        reply.phone = phone
        reply.message = message
        reply.save()

        send_mail('[catalog.mfst.pro] Ваше платье хотят примерить!', message, 'no-reply@mfst.pro', [dress.email], fail_silently=False)

        reply.email_delivered = True
        reply.save()

        dress.buy_tries += 1
        dress.save()

        ok = True
    except Exception, ex:
        print(ex)
        ok = False
    
    result = {"ok": ok,}
    response_data = simplejson.dumps(result)

    mimetype = 'text/plain'
    if 'HTTP_ACCEPT_ENCODING' in request.META.keys():
        if "application/json" in request.META['HTTP_ACCEPT_ENCODING']:
            mimetype = 'application/json'
    return HttpResponse(response_data, mimetype=mimetype)

#dsiaEf
def get_buyers(request, id):
    if request.method != 'POST':
        log.error('[get_buyers] method != POST: %s' % request.method)
        raise Http404

    try:
        access_key = request.POST['access_key']
        dress = Dress.objects.get(pk=id)
    except Exception, ex:
        log.error('[get_buyers] %s' % ex)
        raise Http404

    ok = dress.access_key == access_key
    buyers = []

    try:
        if ok:
            replies = Reply.objects.filter(dress_id=dress.id)
            for reply in replies:
                buyers.append({"fio":reply.fio, "phone":reply.phone, "email":reply.email, "date":reply.date.isoformat()})


        result = {"ok": ok, "buyers": buyers}
        response_data = simplejson.dumps(result)
    except Exception, ex:
        log.error('[get_buyers.2] %s' % ex)
        response_data = simplejson.dumps({})
        pass

    mimetype = 'text/plain'
    if 'HTTP_ACCEPT_ENCODING' in request.META.keys():
        if "application/json" in request.META['HTTP_ACCEPT_ENCODING']:
            mimetype = 'application/json'

    return HttpResponse(response_data, mimetype=mimetype)

@permission_required('emailing')
def emailer(request):
    if request.method=="POST":
        message = request.POST['message']
        subject = request.POST['subject']
        type = request.POST['type']
        if type=="list":
            emails = set([e.strip() for e in request.POST['emails'].split()])
        else:
            reply_emails = [r['email'] for r in Reply.objects.values("email").distinct()]
            dress_emails = [r['email'] for r in Dress.objects.values("email").distinct()]
            emails = reply_emails + dress_emails
        results = []
        for email in emails:
            reason = ""
            try:
                ok = send_mail(subject=subject, message=message, from_email="catalog.mfst.pro <no-reply@mfst.pro>", recipient_list = [email], fail_silently=False)
            except Exception, ex:
                ok = False
                reason = str(ex)
            results.append({"email":email, "ok":"ok" if ok else "failed", "reason": reason})
        response_data = simplejson.dumps(results)

        mimetype = 'text/plain'
        if 'HTTP_ACCEPT_ENCODING' in request.META.keys():
            if "application/json" in request.META['HTTP_ACCEPT_ENCODING']:
                mimetype = 'application/json'
        return HttpResponse(response_data, mimetype=mimetype)
    else:
        return render_to_response('emailer.html', {}, context_instance=RequestContext(request))

def send_sms():
    pass