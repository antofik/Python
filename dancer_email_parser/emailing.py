# coding=utf-8
import smtplib
from email.mime.text import MIMEText
import db
import mysql.connector
import time

me = 'no-reply@mfst.pro'
password = 'no-reply!!!$'

def main():
    template = open('email_template.html').read()
    conn = connect()
    dbconn = db.get_connection()

    i = 0
    while True:
        emails = get_emails(dbconn)
        #emails = [('antofik@gmail.com',)]
        for (email,) in emails:
            i += 1
            print '%s %s' % (i, email)
            try:
                sendEmail(email, template, conn)
                updateEmailStatus(dbconn, email, 1)
            except Exception, ex:
                updateEmailStatus(dbconn, email, -1)
                print email, '>>>>>>>>>>>>>', ex
                pass
            time.sleep(3)
        #break

    dbconn.commit()
    disconnect(conn)
    print 'done.'

def updateEmailStatus(dbconn, email, status=1):
    query = ("update emailing set processed=%s where email='%s'" % (status, email))
    cursor = dbconn.cursor()
    cursor.execute(query, ())
    dbconn.commit()
    cursor.close()

def get_emails(conn):
    emails = []
    cursor = conn.cursor()
    query = ("SELECT email from emailing where processed=0 limit 10")
    cursor.execute(query, (), )
    for (email) in cursor:
        emails.append(email)
    cursor.close()
    return emails


def connect():
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.ehlo()
    s.starttls()
    s.ehlo()
    s.login(me, password)
    return s

def disconnect(conn):
    conn.quit()

def sendEmail(email, template, conn):
    html = template.format(email=email)
    msg = MIMEText(html, 'html')
    msg['Subject'] = u'Каталог бальных платьев'
    msg['From'] = me
    msg['To'] = email
    msg['Reply-To'] = 'contact@mfst.pro'
    msg['Content-Type'] = 'text/html; charset="utf-8"'
    conn.sendmail(me, [email], msg.as_string())

if __name__=="__main__":
    main()