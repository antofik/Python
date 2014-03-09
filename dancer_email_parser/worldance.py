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
    host = '''base.worldance.ru'''
    forum_url = '''/base.php?action=find&page=1&strings=2000&class=nmetter&ass=nmetter&sex=nmetter&age=nmetter&x=39&y=13'''
    try:
        html = loaders.get_page(host,forum_url)
        phones = get_phones(html)
        for phone in phones:
            if '2012-' in phone:
                continue
            print phone
            db.save_phone(cursor, phone, 'worldance', 'worldance')
        conn.commit()
    except Exception, ex:
        print 'Error >>>>>>>>>>>>>>>>> %s' % ex

def get_phones(html):
    return set(re.findall('''[\d()\- ]{7,11}''', html, flags=re.MULTILINE))

if __name__=='__main__':
    main()