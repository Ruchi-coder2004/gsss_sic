import pymysql

def connect_db():
    try:
        connection = pymysql.Connect(host='localhost',user='root',passwd='Ruchi@2004',database='ruchitha_db', port=3306, charset='utf8') # here host='localhost',user='root',passwd='Ruchi@2004',database='ruchitha_db' is necessary
        print('DB Connected')
        return connection
    except:
        print('DB connection failed')

def disconnect_db(connection):
    if connection:
        connection.close

connection = connect_db()
if connection:
    connection.close()
    print('Database Disconnected')