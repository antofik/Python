import base64
import random
import datetime
import threading
import time

class ProxyManager:
    hash = {}
    proxies = []
    initialized = False
    lock = threading.RLock()
    usage = {}
    statistics = {}
    task = {}
    sleep = {}
    bad = []
    credentials = None
    credentials = None
    username = None
    password = None
    initialization_lock = threading.RLock()

    @staticmethod
    def initialize():
        if ProxyManager.initialized:
            return
        ProxyManager.initialization_lock.acquire()
        if ProxyManager.initialized:
            return
        ProxyManager.initialized = True
        #print 'initializing...'
	import os
	print os.path.abspath('.')
        f = open('webparser/proxylist')
        ProxyManager.username, ProxyManager.password = f.readline().strip().split(':')
        ProxyManager.credentials = base64.b64encode('%s:%s' % (ProxyManager.username, ProxyManager.password))
        for line in f:
            if line.startswith('###'):
                break
            if line.startswith('#'):
                continue
            line = line.strip()
            ProxyManager.proxies.append(line)
            ProxyManager.usage[line] = False
            ProxyManager.statistics[line] = 0
            ProxyManager.task[line] = 'ready'
            ProxyManager.sleep[line] = 0
        f.close()
        ProxyManager.initialization_lock.release()

    @staticmethod
    def get(url):
        ProxyManager.initialize()
        if url and url.startswith('http://'):
            url = url.replace('http://','')
            index = url.index('/')
            host = url[0:index]
        else:
            host = '<unknown host>'
        if host not in ProxyManager.hash:
            ProxyManager.hash[host] = HostProxyManager(host, ProxyManager.proxies)
        return ProxyManager.hash[host].get()

class Proxy:
    timeout = 3.0

    def __init__(self, host, manager):
        self.manager = manager
        self.host = host
        self.last = None
        self.busy = False

    def wait(self):
        #print '[%s] wait' % self.host
        if not self.last:
            self.last = datetime.datetime.now()
            #print '[%s] exiting' % self.host
            return
        now = datetime.datetime.now()
        deltatime = int((now - self.last).total_seconds())
        self.last = datetime.datetime.now()
        if deltatime<self.timeout:
            #print '[%s] waiting %s sec' % (self.host, (self.timeout-deltatime))
            ProxyManager.sleep[self.host] += self.timeout - deltatime
            self.setStatus('Sleep')
            time.sleep((self.timeout - deltatime))
            self.setStatus('Ready')

    def setStatus(self, message = None):
        ProxyManager.task[self.host] = message

    def release(self):
        self.setStatus()
        self.manager.release(self)

class HostProxyManager:
    def __init__(self, host, proxies):
        self.host = host
        self.proxies = []
        for item in sorted(proxies, key=lambda v: random.random()):
            proxy = Proxy(item, self)
            self.proxies.append(proxy)
        #print 'initializing proxy for host', host, '\n', 'proxies:', self.proxies


    def get(self):
        selected = None
        i = 0
        while not selected:
            #print 'geting from ', len(self.proxies)
            ProxyManager.lock.acquire()
            for proxy in self.proxies:
                if proxy.host in ProxyManager.bad:
                    continue
                if ProxyManager.usage[proxy.host]:
                    continue
                selected = proxy
                ProxyManager.usage[selected.host] = True
                self.proxies.remove(selected)
                break
            ProxyManager.lock.release()
            if not selected:
                time.sleep(5)
                i += 1
                if i>10:
                    print 'No proxy'
        #print 'got', selected.host
        ProxyManager.initialization_lock.acquire()
        ProxyManager.statistics[selected.host] += 1
        ProxyManager.initialization_lock.release()
        selected.wait()
        return selected

    def release(self, proxy):
        ProxyManager.lock.acquire()
        self.proxies.append(proxy)
        ProxyManager.usage[proxy.host] = False
        ProxyManager.lock.release()
