# coding=utf-8
# Create your views here.
import logging
from django.contrib.auth.decorators import permission_required
from django.http import HttpResponse
from django.shortcuts import render_to_response, redirect
from django.template.context import RequestContext
import httplib
import re
from dancer_email_parser.models import DancerPhone, DancerEmail
import mysql.connector
from mysql.connector import errorcode

def get_page(host, url):
    connection = httplib.HTTPConnection(host)
    connection.request('GET', url)
    response = connection.getresponse()
    data = response.read()
    data = data.decode('cp1251').encode('utf8')
    return data

# <a href="viewtopic.php?p=5755#5755">
def get_topics(html):
    return set(['/' + uri for uri in re.findall('''<a href="(viewtopic\.php\?p=.{10,100})">''', html, flags=re.MULTILINE)])

# <br/>Телефон: 89266889264<br/>
def get_phones(html):
    return set(re.findall('''<br/>Телефон:([^<>]{5,32})<br/>''', html, flags=re.MULTILINE))


#<br/>E-mail: muchacha21@mail.ru<br/>
def get_emails(html):
    return set(re.findall('''<br/>E-mail:([^<>]{5,64})<br/>''', html, flags=re.MULTILINE))

@permission_required('emailing')
def machaon(request):
    start = 0
    end = 210#4160
    topics = []
    host = '''partner.machaon-dance.ru'''
    forum_mask_url = '''/viewforum.php?f=1&topicdays=0&start=%s'''
    for i in range(start,end):
        try:
            html = get_page(host,forum_mask_url % (i*20))
            topics = get_topics(html)
            for topic in topics:
                print '%s/%s %s' % (i,end, topic)
                html = get_page(host, topic)
                phones = get_phones(html)
                emails = get_emails(html)
                for phone in phones:
                    item = DancerPhone()
                    item.raw = phone
                    item.source = '%s %s' % (i, topic)
                    item.data = topic
                    item.save()
                for email in emails:
                    item = DancerEmail()
                    item.raw = email
                    item.source =host
                    item.data = topic
                    item.save()
        except Exception, ex:
            print '>>>>>>>>>>>>>>>>>>>>>>>>>> %s' % ex
            pass
    phones = DancerPhone.objects.all()
    emails = DancerEmail.objects.all()
    return render_to_response('machaon.html', {'phones':phones, 'emails':emails, 'topics':topics}, context_instance=RequestContext(request))

def emailing(request, email):
    print('emailing with <%s>' % email)
    ok = 'ok'
    try:
        conn = get_connection()
        query = ("insert into emailing (email) values ('{email}')".format(email=email, date=''))
        cursor = conn.cursor()
        cursor.execute(query, ())
        conn.commit()
        cursor.close()
        conn.close()
    except Exception, ex:
        logging.error(ex)
        ok += str(ex)
        ok += "\n"
    try:
        conn = get_connection()
        query = ("update emailing set state='viewed' where state='initial' and email='{email}'".format(email=email))
        cursor = conn.cursor()
        cursor.execute(query, ())
        conn.commit()
        cursor.close()
        conn.close()
    except Exception, ex:
        logging.error(ex)
        ok += str(ex)
        ok += "\n"
    return HttpResponse(ok)

def get_connection():
    connection = None
    try:
        connection = mysql.connector.connect(user='root', host='176.9.142.3', password='root', database='dancer_contacts')
        #connection = mysql.connector.connect(user='dataminer', host='127.0.0.1', password='data-mining@@@', database='dancer_contacts')
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong your username or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exists")
        else:
            print 'Cannot connect to database: %s' % err
    return connection


def click(request, email):
    print('clicking with <%s>' % email)
    try:
        conn = get_connection()
        query = ("update emailing set state='clicked' where email='{email}' ".format(email=email))
        cursor = conn.cursor()
        cursor.execute(query, ())
        conn.commit()
        cursor.close()
        conn.close()
    except Exception, ex:
        logging.error(ex)
    return redirect('/')


def smsing(request, phone, status):
    ok = 'ok'
    try:
        conn = get_connection()
        query = ("update smsing set state='{status}' where phone='{phone}' ".format(phone=phone, status=status))
        cursor = conn.cursor()
        cursor.execute(query, ())
        conn.commit()
        cursor.close()
        conn.close()
    except Exception, ex:
        logging.error(ex)
        ok = 'failed'
    return HttpResponse(ok)