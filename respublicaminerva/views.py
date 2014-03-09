from django.contrib.auth import authenticate, login
from django.http import HttpResponse, Http404
from django.template import Template, Context, RequestContext
from django.shortcuts import render_to_response, redirect
import logging
from django.utils import simplejson

def home(request):    
    return render_to_response('home.html', {}, context_instance=RequestContext(request))

def check(request):    
    return render_to_response('check.html', {}, context_instance=RequestContext(request))

def online(request):    
    return render_to_response('notimplemented.html', {}, context_instance=RequestContext(request))

def news(request):    
    return render_to_response('notimplemented.html', {}, context_instance=RequestContext(request))

def partners(request):    
    return render_to_response('partners.html', {}, context_instance=RequestContext(request))

def contact(request):    
    return render_to_response('contacts.html', {}, context_instance=RequestContext(request))

def prices(request):    
    return render_to_response('notimplemented.html', {}, context_instance=RequestContext(request))

def shop(request):    
    return render_to_response('notimplemented.html', {}, context_instance=RequestContext(request))

def about(request):    
    return render_to_response('about.html', {}, context_instance=RequestContext(request))

def schedule(request):
    return render_to_response('schedule.html', {}, context_instance=RequestContext(request))

def test(request):
    return render_to_response('test.html', {}, context_instance=RequestContext(request))

def ajax_login(request):
    if request.method!="POST":
        raise Http404
    ok = False

    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            ok = True

    result = {'ok': ok }
    response_data = simplejson.dumps(result)

    mimetype = 'text/plain'
    if 'HTTP_ACCEPT_ENCODING' in request.META.keys():
        if "application/json" in request.META['HTTP_ACCEPT_ENCODING']:
            mimetype = 'application/json'
    return HttpResponse(response_data, mimetype=mimetype)
