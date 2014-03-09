import httplib
import traceback
import urllib
import urllib2
import time
from webparser import parser
from webparser.proxy import ProxyManager
from clint.textui import colored
import traceback

class loader:
    max_tries = 10
    defaultHost = 'http://www.aliexpress.com'

    def __init__(self, host):
        self.host = host

    def get(self, url):
        data = None
        if url.startswith('/'):
            url = loader.defaultHost + url

        if ProxyManager.credentials:
            headers = {"Proxy-Authorization": 'Basic ' + str(ProxyManager.credentials)}
        else:
            headers = None
        tries = 0
        while True:
            proxy = ProxyManager.get(url)
            proxy.setStatus('get %s' % url)
            #print 'using proxy ', proxy.host
            connection = httplib.HTTPConnection(proxy.host)
            try:
                if headers:
                    connection.request('GET', url, headers=headers)
                else:
                    connection.request('GET', url)
                response = connection.getresponse()
                #print '!' * 800
                #print response.msg()
                data = response.read()
                if response.status==111:
                    ProxyManager.bad.append(proxy.host)
                    raise Exception('Proxy %s added to blacklist' % proxy.host)
                if response.status==301:
                    newurl = parser.get_value(r'Location: (.*?\.html)', str(response.msg))
                    proxy.setStatus('[301] moved to %s' % newurl)
                    proxy.release()
                    return self.get(newurl)
                if response.status==404:
                    proxy.setStatus('[404] not found %s' % url)
                    proxy.release()
                    return ''
                if response.status==413:
                    proxy.setStatus('[413] not found %s' % url)
                    proxy.release()
                    colored.red('!'*10000)
                    traceback.print_stack()
                    return ''
                if str(response.status).startswith('4'):
                    proxy.setStatus('[%s] error %s' % (response.status, url))
                    proxy.release()
                    #return '[%s] Error' % response.status
                    raise Exception('[status:%s] <%s>\n%s' % (response.status, url, response.msg))

                if not str(response.status).startswith('2'):
                    proxy.setStatus('[%s] Error at %s' % (response.status, url))
                    raise Exception('[status:%s] <%s>\n%s' % (response.status, url, response.msg))
                if len(data)<5:
                    proxy.setStatus('Empty response at %s' % url)
                    print 'Empty response at <%s>' % url
                if ('aliexpress' in url) and ('cross-domain' not in url) and (not data.rstrip().endswith('</html>')) and (not 'http://translate.yandex.ru/' in url):
                    print '<<<<<<<<<<<<<<<<<<<<<<<<<<<<<,,partial response.>>>>>>>>>>>>>>>>>>>>>>>>>>\n%s' % url, data[-300:]
                break
            except Exception, e:
                #traceback.print_exc()
                proxy.release()
                print 'Error in get [%s]:' % proxy.host, e
                if 'refused' in str(e) \
                    or 'No route to host' in str(e) \
                    or 'forcibly' in str(e) \
                    or 'reset by peer' in str(e):
                    print 'Blocking proxy %s' % proxy.host
                    ProxyManager.bad.append(proxy.host)
                tries += 1
                if tries>loader.max_tries:
                    print 'Skipping link...'
                    #todo mark proxy as bad
                    break
            finally:
                proxy.release()
            time.sleep(10)
            try:
                connection.close()
                del connection
            except:
                pass
        return data

    def post(self, url, **params):
        connection = httplib.HTTPConnection(self.host)
        params = urllib.urlencode(params)
        headers = {"Content-type": "application/x-www-form-urlencoded", 'Accept-Encoding':'deflate'}
        connection.request('POST', url, params, headers)
        response = connection.getresponse()
        data = response.read()
        connection.close()
        return data

    def save(self, url, local):
        if url.startswith('/'):
            url = 'http://www.aliexpress.com' + url
        if ProxyManager.credentials:
            headers = {"Proxy-Authorization": 'Basic ' + str(ProxyManager.credentials)}
        else:
            headers = None
        tries = 0
        while True:
            try:
                proxy = ProxyManager.get(url)
                proxy.setStatus('Downloading image at %s' % url)
                req = urllib2.Request(url, headers=headers)
                proxy_handler = urllib2.ProxyHandler({'http': 'http://%s/' % proxy.host})
                proxy_auth_handler = urllib2.ProxyBasicAuthHandler()
                proxy_auth_handler.add_password('realm', proxy.host, ProxyManager.username, ProxyManager.password)
                opener = urllib2.build_opener(proxy_handler, proxy_auth_handler)
                f = opener.open(req)
                l = open(local, 'wb')
                l.write(f.read())
                l.close()
                del l
                del f
                break
            except Exception, e:
                if 'Not Found' in str(e):
                    return
                print '[%s] Error while saving file' % proxy.host, url, e
                #traceback.print_exc()
                tries += 1
                if tries>loader.max_tries:
                    raise
            finally:
                proxy.release()
            time.sleep(10)

    def save_direct(self, url, local):
        if url.startswith('/'):
            url = loader.defaultHost + url
        urllib.urlretrieve(url, local)
