import db

def main():
    conn = db.get_connection()
    cursor = conn.cursor()

    for line in open('email.txt'):
        if len(line)>5:
            db.save_phone(cursor, line, 'pasha.old', 'pasha.old')
            print line

    conn.commit()
    cursor.close()
    conn.close()
    print 'done.'

if __name__=='__main__':
    main()