#!/usr/bin/python
# coding=utf-8
__author__ = 'anton'

from optparse import OptionParser
parser = OptionParser()
parser.add_option("-s", "--send", action="store_false", default=True, dest="DEBUG")
(options, args) = parser.parse_args()
DEBUG = options.DEBUG



if not DEBUG:
    import sms24x7
import db

login = 'antofik@mail.ru'
password = 'inevsms24x7'
url = 'http://catalog.mfst.pro/smsing/register/%p/%d'
mask = 63

def main():
    if not DEBUG:
        smsapi = sms24x7.smsapi(login, password)
        smsapi.login()
    else:
        smsapi = None

    i = 0
    while True:
        phones = get_phones()
        if not phones:
            break
        for phone in phones:
            i += 1
            print '%s>%s' % (i, phone)
            if not send_sms(smsapi, phone):
                failed(phone)
            else:
                done(phone)
        if DEBUG:
            break

    print 'done.'

def failed(phone):
    conn = db.get_connection()
    query = ("update smsing set processed=-1 where phone='%s'" % phone)
    cursor = conn.cursor()
    cursor.execute(query, ())
    conn.commit()
    cursor.close()
    conn.close()

def done(phone):
    conn = db.get_connection()
    query = ("update smsing set processed=1 where phone='%s'" % phone)
    cursor = conn.cursor()
    cursor.execute(query, ())
    conn.commit()
    cursor.close()
    conn.close()

def get_phones():
    conn = db.get_connection()
    phones = []
    cursor = conn.cursor()
    query = ("SELECT phone from smsing where processed=0 limit 10")
    cursor.execute(query, (), )
    for (phone,) in cursor:
        phones.append(phone)
    cursor.close()
    conn.close()
    return phones

def send_sms(api, phone):
    if DEBUG:
        return True
    try:
        api.push_msg(u'Купить или продать бальное платье? catalog.mfst.pro - лучшее решение!', phone, dlr_url=url, dlr_maks=mask)
        return True
    except:
        return False

if __name__=="__main__":
    main()
