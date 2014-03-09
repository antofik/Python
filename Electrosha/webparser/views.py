# Create your views here.
import datetime
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
import thread
from aliexpress.aliexpress import aliexpress
from webparser.models import *
from webparser.proxy import ProxyManager

parser = None
time = None
gcount = 0
gcount_done = 0

def parse(args):
    global parser
    print 'Parsing...'
    parser.parse()

def index(request):
    global parser
    global time, gcount, gcount_done
    if not parser:
        print 'Starting new session'
        clear_db()
        parser = aliexpress()
        time = datetime.datetime.now()

    #return HttpResponse('ok')

    count = 0
    count_done = 0
    if parser.done:
        print 'Parsing is finished. Starting new one'
        thread.start_new(parse, (None,))
        data = []
    else:
        data = parser.categories
    count_done = aliexpress.done_count
    now = datetime.datetime.now()
    delta = (now - time).total_seconds() + 0.0001
    time = now
    speed = round(10.0*(count - gcount) / delta)/10.0
    speed_done = round(10.0*(count_done - gcount_done) / delta)/10.0
    gcount = count
    gcount_done = count_done

    proxies = []
    for p in ProxyManager.proxies:
        item = proxyData()
        item.host = p
        item.busy = ProxyManager.usage[p]
        item.count = ProxyManager.statistics[p]
        item.sleep = ProxyManager.sleep[p]
        if p in ProxyManager.task:
            item.task = ProxyManager.task[p]
        proxies.append(item)

    return render_to_response('index.html', {
        'count': count,
        'count_done': count_done,
        'speed': speed,
        'speed_done': speed_done,
        'done': parser.done,
        'data':data,
        'proxy':proxies,
    },
        context_instance=RequestContext(request))

class proxyData:
    def __init__(self):
        pass
