# coding=utf-8
__author__ = 'anton'

import re
import db

def main():
    conn = db.get_connection()
    cursor = conn.cursor()

    for line in open('russianmaster.txt'):
        for email in get_emails(line):
            print email
            db.save_email(cursor, email, 'russianmaster', line)
        for phone in get_phones(line):
            print phone
            db.save_phone(cursor, phone, 'russianmaster', line)

    conn.commit()
    cursor.close()
    conn.close()
    print 'done.'

def get_emails(html):
    return set(re.findall('''\t([\w\.]*@[\w\.]*)\t''', html, flags=re.MULTILINE))

def get_phones(html):
    return set(re.findall('''[78]\-? ?\(?\d{3}\)? ?\-?\d{3} ?\-?\d{2} ?\-?\d{2}''', html, flags=re.MULTILINE))

if __name__=='__main__':
    main()