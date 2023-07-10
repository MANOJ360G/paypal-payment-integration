

import sqlite3

conn = sqlite3.connect('test.db')

# CREATE
try:
    conn.execute('''CREATE TABLE ipn (unix INT(10), 
    payment_date VARCHAR(30), username VARCHAR(20), 
    last_name VARCHAR(30), payment_gross FLOAT(6,2),
     payment_fee FLOAT(6,2), payment_net FLOAT(6,2), 
     payment_status VARCHAR(15), txn_id VARCHAR(25)); ''')
    
except Exception as e:
    print(e)


def add_ipn(
    payer_email,
    unix, 
    payment_date, 
    username, 
    last_name, 
    payment_gross, 
    payment_fee, 
    payment_net, 
    payment_status, 
    txn_id
):

    # c,conn = connection()
    conn.execute("INSERT INTO ipn (unix, payment_date, username, last_name, payment_gross, payment_fee, payment_net, payment_status, txn_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
                (unix, payment_date, username, last_name, payment_gross, payment_fee, payment_net, payment_status, txn_id))
    conn.commit()
    conn.close()
    # c.collect()
    