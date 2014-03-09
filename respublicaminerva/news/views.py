from django.http import HttpResponse
from django.template import Template, Context, RequestContext
from django.shortcuts import render_to_response, redirect
from models import *

def newslist(request):    
    items = Item.objects.select_related('news').all()
    return render_to_response('news.html', {'items':items}, context_instance=RequestContext(request))
