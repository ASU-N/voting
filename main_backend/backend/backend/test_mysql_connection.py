import pymysql

connection = pymysql.connect(
    host='localhost',
    user='root',
    password='aarati123',
    database='voting_db'
)

try:
    with connection.cursor() as cursor:
        cursor.execute('SELECT DATABASE();')
        db = cursor.fetchone()
        print(f'Connected to database: {db}')
finally:
    connection.close()
