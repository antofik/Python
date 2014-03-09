# coding=utf-8
__author__ = 'anton'

import re
import db
import loaders
import time

def main():
    conn = db.get_connection()
    cursor = conn.cursor()
    parse(cursor, conn)
    cursor.close()
    conn.close()
    print 'done.'

def parse(cursor, conn):
    host = '''vk.com'''
    forum_url = '''/topic-445047_13367963'''
    for i in xrange(0,7):
        try:
            html = loaders.post_page(host,forum_url, {'al':1, 'offset':i*20, 'part':1}, {'Cookie:':'remixchk=5; remixdt=0; remixlang=0; remixrec_sid=; remixsid=26322cd9dfac2f0d392f0d1e6db487ea5e74c6f8b97c146bf88af9cdbb10; remixreg_sid=; remixseenads=1; remixflash=11.3.300'})
            phones = get_phones(html)
            for phone in phones:
                print phone
                db.save_phone(cursor, phone, 'vk', forum_url)
            conn.commit()
        except Exception, ex:
            print 'Error >>>>>>>>>>>>>>>>> %s' % ex
        time.sleep(1.3)

def get_phones(html):
    return set(re.findall('''[78]\-? ?\(?\d{3}\)? ?\-?\d{3} ?\-?\d{2} ?\-?\d{2}''', html, flags=re.MULTILINE))

if __name__=='__main__':
    main()