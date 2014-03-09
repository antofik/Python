# coding=utf-8
__author__ = 'anton'

import re
import db
import loaders

def main():
    conn = db.get_connection()
    cursor = conn.cursor()
    parse(cursor, conn)
    cursor.close()
    conn.close()
    print 'done.'

def parse(cursor, conn):
    host = '''www.forkids.ru'''
    forum_mask_url = '''/dance/dancepartner/anketa/%s.html'''
    for i in range(665,1170):
        try:
            html = loaders.get_page(host,forum_mask_url % i)
            phones = get_phones(html)
            emails = get_emails(html)
            for phone in phones:
                print i, ' ', phone
                db.save_phone(cursor, phone, 'forkids', i)
            for email in emails:
                if email=='forkids2009@gmail.com':
                    continue
                print i, ' ', email
                db.save_email(cursor, email, 'forkids', i)
            conn.commit()
        except Exception, ex:
            print 'Error >>>>>>>>>>>>>>>>> %s' % ex

def get_phones(html):
    return set(re.findall('''Телефон:</TD>\n<TD class=text12>([^<>]{5,32})</TD></TR>''', html, flags=re.MULTILINE))

def get_emails(html):
    return set(re.findall('''"mailto:([^<>"]{5,32})"''', html, flags=re.MULTILINE))

if __name__=='__main__':
    main()