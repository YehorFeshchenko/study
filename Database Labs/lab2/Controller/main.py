import psycopg2


def get_password():
    f = open(r"D:\Job\Apps\password.txt", "r")
    data = f.read()
    f.close()
    return data


conn = psycopg2.connect(dbname='Lab1_db', user='postgres', password=get_password(), host='localhost')
cursor = conn.cursor()
cursor.execute('SELECT * FROM groups')
records = cursor.fetchone()
print(records)
cursor.close()
conn.close()
