import django.contrib.auth
from django.http import HttpResponse
from django.template import Template, Context, RequestContext
from django.shortcuts import render_to_response, redirect
from django.contrib.auth.decorators import login_required
import logging
import forms
import models
from check.models import *
from auth.models import *
import pprint

@login_required
def profile(request):
    try:
        profile = request.user.get_profile()
    except:
        profile = UserProfile.objects.create(user=request.user)
    
    orders = Item.objects.select_related('check').filter(user=request.user)
    pprint.pprint(orders)
    
    return render_to_response(
        'profile.html',
        {
            'profile': profile,
            'orders' : orders,
        },
        context_instance=RequestContext(request)
    )
