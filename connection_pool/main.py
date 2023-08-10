from connection_pool import ConnectionPool

creds = {
    'username': 'postgres',
    'host': '127.0.0.1:',
    'dbname': ''
}

pool = ConnectionPool(creds)



def get_details():
    cp = pool.get_connection()
    cursor_obj = cp.cursor()
    result = cursor_obj.execute('')
    print(result)
    pool.close_connection(cp)


get_details()