# coding=utf-8
import logging
from django.core.mail import send_mail
from django.http import HttpResponse, Http404
from django.template import Template, Context, RequestContext
from django.shortcuts import render_to_response, redirect, render
from django.utils import simplejson
from models import *
import datetime
from django import forms
from django.http import HttpResponseRedirect
import smtplib
from email.mime.text import MIMEText

def checkform(request):    
    if request.method == 'POST':
        form = CheckForm(request.POST)
        if form.is_valid():
            order = Item.objects.select_related('check').filter(code=request.POST['code'])
            if order:
                return render(request, 'check.html', {
                    'order': order,
                    'form': form,
                    'diff': (order[0].date_ready.date() - datetime.date.today()).days,
                    'user': request.user,
                })
            else:
                return render(request, 'check.html', {
                    'order_not_found': True,
                    'form': form,
                    'user': request.user,
                })
        else:
            form2 = QuestionForm()
            try:
                msg = MIMEText(request.POST['text'])
                msg['Subject'] = u'Сообщение fabricartis.ru'
                msg['From'] = request.user.email
                msg['To'] = 'contact@fabricartis.ru'
                s = smtplib.SMTP('localhost')
                s.sendmail('contact@fabricartis.ru', request.user.email, msg.as_string())
                s.quit()
                error = None
            except:
                error = "Ошибка отправки письма"
            return render(request, 'check.html', {
                'message_sent': True,
                'form': form2,
                'user': request.user,
                'error': error,
            })
    else:
        form = CheckForm()

    return render(request, 'check.html', {
        'form': form,
        'user': request.user,
    })

def send_message(from_email, message):
    try:
        send_mail(u'Сообщение fabricartis.ru', message, from_email, ['contact@fabricartis.ru'], fail_silently=False)
        return True
    except:
        return False


def check_postmessage(request):
    if request.method!="POST":
        raise Http404

    message = request.POST['message']
    from_email = request.user.email
    ok = send_message(from_email, message)

    result = {'ok': ok }
    response_data = simplejson.dumps(result)

    mimetype = 'text/plain'
    if 'HTTP_ACCEPT_ENCODING' in request.META.keys():
        if "application/json" in request.META['HTTP_ACCEPT_ENCODING']:
            mimetype = 'application/json'
    return HttpResponse(response_data, mimetype=mimetype)


def check_postorder(request):
    if request.method!="POST":
        raise Http404

    code = request.POST['code']
    print "Code=", code
    order = Item.objects.select_related('check').filter(code=code)
    print order
    if order:
        ok = True
        days = (order[0].date_ready.date() - datetime.datetime.now().date()).days
    else:
        ok = False
        days = None

    result = {
        'ok': ok,
        'days': days,
    }
    response_data = simplejson.dumps(result)

    mimetype = 'text/plain'
    if 'HTTP_ACCEPT_ENCODING' in request.META.keys():
        if "application/json" in request.META['HTTP_ACCEPT_ENCODING']:
            mimetype = 'application/json'
    return HttpResponse(response_data, mimetype=mimetype)


class CheckForm(forms.Form):
    code = forms.CharField(max_length=16)

class QuestionForm(forms.Form):
    text = forms.CharField(max_length=1024)

