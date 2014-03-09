import httplib
import urllib
import zlib

__author__ = 'anton'

def get_page(host, url):
    connection = httplib.HTTPConnection(host)
    connection.request('GET', url)
    response = connection.getresponse()
    data = response.read()
    try:
        data = data.decode('cp1251').encode('utf8')
    except:
        pass
    return data

def post_page(host, url, params, add_headers):
    connection = httplib.HTTPConnection(host)
    params = urllib.urlencode(params)
    headers = {"Content-type": "application/x-www-form-urlencoded", 'Accept-Encoding':'deflate, chunked'}
    headers.update(add_headers)
    connection.request('POST', url, params, headers)
    response = connection.getresponse()
    data = response.read()
    try:
        data = zlib.decompress(data)
        data = data.decode('cp1251').encode('utf8')
    except Exception, ex:
        print ex
    return data
