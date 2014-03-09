import mysql.connector
from mysql.connector import errorcode
import formatter

def get_connection():
    connection = None
    try:
        connection = mysql.connector.connect(user='root', host='176.9.142.3', password='root', database='dancer_contacts')
        #connection = mysql.connector.connect(user='dataminer', host='176.9.142.3', password='data-mining@@@', database='dancer_contacts')
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong your username or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exists")
        else:
            print(err)
    return connection

add_phone = ("INSERT INTO phones (raw, data, source) VALUES (%s, %s, %s)")
add_email = ("INSERT INTO emails (raw, data, source) VALUES (%s, %s, %s)")

def save_phone(cursor, raw, source, data):
    phone = formatter.clean_phone(raw)
    if phone is None:
        return
    values = (phone, data, source)
    cursor.execute(add_phone, values)

def save_email(cursor, raw, source, data):
    email = formatter.clean_email(raw)
    if email is None:
        return
    values = (email, data, source)
    cursor.execute(add_email, values)
