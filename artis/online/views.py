# coding=utf-8
from django.core.mail import send_mail
from django.http import HttpResponse, Http404
from django.template import Template, Context, RequestContext
from django.shortcuts import render_to_response, redirect
import logging
from check.models import Item
from models import *
import datetime

def measures(request):
    if request.method!="POST":
        raise Http404
    measures = []
    if request.user.is_authenticated():
        values = request.POST.getlist('values[]')
        for item in values:
            (type_id, value) = item.split()
            entries = Measure.objects.filter(type_id = type_id, user_id = request.user.id)
            for entry in entries:
                entry.delete()
            m = Measure.objects.create(type_id = type_id, user_id = request.user.id, value = value)
            m.save()
            measures.append(m)
    ok = send_measures(request.user, measures)

    return render_to_response('empty.html', {}, context_instance=RequestContext(request))

def send_measures(user, measures):
    try:
        message = u'Мерки пользователя %s (%s %s)\n' % (user.username, user.last_name if not None else "фамилия не указана", user.first_name)
        for measure in measures:
            message += u'\n    %s - %sсм' % (measure.type.name, measure.value)

        try:
            message += u'\n\nПользователь сделал следующие заказы:'
            for order in Item.objects.filter(user=user):
                message += u'\n    №%s %s %s - %s' % (order.code, order.added.date(), order.title, order.text)
        except Exception, e:
            print e
            logging.error(str(e))

        try:
            message += u'\n\nПользователь записан на слудующие примерки:'
            for entry in UserEntry.objects.select_related('type').filter(user=user):
                message += u'\n %s на время %s-%s %s ' % (entry.date, entry.type.start.strftime('%H:%M'), entry.type.end.strftime('%H:%M'), entry.description)
        except Exception, e:
            print e
            logging.error(str(e))

        from_email = user.email
        send_mail(u'Сообщение fabricartis.ru', message, from_email, ['contact@fabricartis.ru', 'antofik@gmail.com'], fail_silently=False)
        return True
    except Exception, e:
        print e
        logging.error(str(e))
        return False

def entry_list(request, year, month, day):    
    user = request.user
    try:
        date = datetime.date(int(year), int(month), int(day))
    except:
        raise Http404

    if request.GET['action']:
        action = request.GET['action']
        if action == 'remove':
            entries = UserEntry.objects.select_related('type').filter(date=date, user_id=user.id, type_id=request.GET['type'])
            if entries:
                entries[0].delete()
        if action == 'subscribe':
            entries = UserEntry.objects.select_related('type').filter(date=date, user_id=user.id, type_id=request.GET['type'])
            if not entries:
                e = UserEntry.objects.create(user_id = user.id, type_id = request.GET['type'], date = date, description = '')
                e.save()
    
    entry_types = EntryType.objects.all()

    items = []
    
    for entry in entry_types:
        entry.empty = True
        entry.type = 'записаться'
        items.append(entry)
        pass

    if user.is_authenticated():
        entries = UserEntry.objects.select_related('type').filter(date=date)
        for i in entries:
            e = get_entry(items, i.type.id)
            e.empty = False
            if i.user==user:
                e.type = 'вы записаны'
                e.mine = True
            else:
                e.type = 'занято'
    else:
        pass

    return render_to_response('entry_list.html', {'entries':items, 'date': date}, context_instance=RequestContext(request))

def month_to_string(month):
    values = (u'Январь',
              u'Февраль',
              u'Март',
              u'Апрель',
              u'Май',
              u'Июнь',
              u'Июль',
              u'Август',
              u'Сентябрь',
              u'Октябрь',
              u'Ноябрь',
              u'Декабрь',)
    return values[month]

def online(request):    
    measure_types = MeasureType.objects.all()
    entry_types = EntryType.objects.all()
    user = request.user
    
    items = []

    delete = False
    create = False
    if delete:
        for e in MeasureType.objects.all():
            e.delete()
    if create:
        e = MeasureType.objects.create(name = 'Рост', description = 'Рост в сантиметрах')
        e.save()
        e = MeasureType.objects.create(name = 'Обхват талии (ОТ)', description = 'Обхват талии (ОТ) измеряется по естественной линии талии, плотно обхватив талию сантиметровой лентой')
        e.save()
        e = MeasureType.objects.create(name = 'Обхват шеи (ОШ)', description = 'Обхват талии (ОТ) измеряется по естественной линии талии, плотно обхватив талию сантиметровой лентой')
        e.save()
        e = MeasureType.objects.create(name = 'Обхват груди (ОТ)', description = 'Обхват талии (ОТ) измеряется по естественной линии талии, плотно обхватив талию сантиметровой лентой')
        e.save()
        e = MeasureType.objects.create(name = 'Обхват бедёр (ОТ)', description = 'Обхват талии (ОТ) измеряется по естественной линии талии, плотно обхватив талию сантиметровой лентой')
        e.save()
        e = MeasureType.objects.create(name = 'Обхват ноги (ОТ)', description = 'Обхват талии (ОТ) измеряется по естественной линии талии, плотно обхватив талию сантиметровой лентой')
        e.save()
    if delete:
        for e in EntryType.objects.all():
            e.delete()

    if create:
        e = EntryType.objects.create(start='12:00', end='13:00')
        e.save()
        e = EntryType.objects.create(start='13:00', end='14:00')
        e.save()
        e = EntryType.objects.create(start='14:00', end='15:00')
        e.save()
    
    for entry in entry_types:
        entry.empty = True
        entry.type = 'записаться'
        items.append(entry)
        pass

    if user.is_authenticated():
        entries = UserEntry.objects.select_related('type').filter(date=datetime.date.today())
        for i in entries:
            e = get_entry(items, i.type.id)
            e.empty = False
            if i.user==user:
                e.type = 'вы записаны'
                e.mine = True
            else:
                e.type = 'занято'
    else:
        pass
        
    measures = Measure.objects.filter(user_id=user.id)
    measure_types = list(MeasureType.objects.all())
    if user.is_authenticated():
        for type in measure_types:
            m = get_measure(measures, type.id)            
            if not m:
                m = Measure.objects.create(type_id = type.id, user_id = user.id)
                m.save()                
            type.measure = m
   
    return render_to_response(
        'online.html', {
            'entries':items,
            'measure_types':measure_types,
            'date': datetime.date.today(),
            'is_authenticated': user.is_authenticated()
        },
        context_instance=RequestContext(request)
    )
    

def get_measure(entries, id):
    for e in entries:
        if e.type.id == id:
            return e
    return None

def get_entry(entries, id):
    for e in entries:
        if e.id == id:
            return e
    return None
