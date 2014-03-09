import re
import traceback
import urllib2
from webparser import http

loader = http.loader('translate.yandex.ru')

def translate(text):
    result = ''
    while text:
        try:
            index = text.index(' ', 250)
            part = text[:index]
            text = text[index:]
            result += ' ' + translateYandex(part)
        except:
            try:
               result += ' ' + translateYandex(text)
            except:
               pass
            break
    return result

def translateYandex(text):
    if not text:
        return ''
    try:
        text = urllib2.quote(text.encode('utf8'))
        link = 'http://translate.yandex.ru/tr.json/translate?lang=en-ru&text=%s&srv=tr-text&reason=paste' % text
        data = loader.get(link)
        data = re.sub(r'^"+|"+', '', data)
        return data
    except Exception, e:
        print 'Error while translating', e
        traceback.print_exc()
        return text
