# coding=utf-8
import re
import db
import loaders

def main():
    conn = db.get_connection()
    cursor = conn.cursor()
    parse(0,cursor, conn)
    cursor.close()
    conn.close()
    print 'done.'

def parse(start, cursor, conn):
    host = '''partner.machaon-dance.ru'''
    forum_mask_url = '''/viewforum.php?f=2&topicdays=0&start=%s'''
    for i in range(start,10000):
        try:
            html = loaders.get_page(host,forum_mask_url % (i*20))
            topics = get_topics(html)
            if not topics:
                break
            for topic in topics:
                position = '%s %s' % (i, topic)
                print position
                html = loaders.get_page(host, topic)
                phones = get_phones(html)
                emails = get_emails(html)
                for phone in phones:
                    db.save_phone(cursor, phone, 'script', position)
                for email in emails:
                    db.save_email(cursor, email, 'script', position)
                conn.commit()
        except Exception, ex:
            print 'Error >>>>>>>>>>>>>>>>> %s' % ex

def get_topics(html):
    return set(['/' + uri for uri in re.findall('''<a href="(viewtopic\.php\?p=.{10,100})">''', html, flags=re.MULTILINE)])

def get_phones(html):
    return set(re.findall('''<br/>Телефон:([^<>]{5,32})<br/>''', html, flags=re.MULTILINE))

def get_emails(html):
    return set(re.findall('''<br/>E-mail:([^<>]{5,64})<br/>''', html, flags=re.MULTILINE))

if __name__=='__main__':
    main()