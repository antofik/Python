from django.http import HttpResponse
from django.template import Template, Context, RequestContext
from django.shortcuts import render_to_response, redirect
from models import *

def pricelist(request):    
    items = Item.objects.select_related('category').all()
    return render_to_response('prices.html', {'items':items}, context_instance=RequestContext(request))
