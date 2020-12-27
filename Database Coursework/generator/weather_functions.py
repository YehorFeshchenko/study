import psycopg2
import datetime


def get_date(dt, tz):
    date = dt + tz
    return datetime.datetime.fromtimestamp(date)


def check_city_exists(id_, connection):
    try:
        cursor_ = connection.cursor()

        postgres_insert_query = """ SELECT * from city where api_city_id = %s"""
        record_to_insert = (id_,)
        cursor_.execute(postgres_insert_query, record_to_insert)
        record = cursor_.fetchone()
        if record is None:
            return -1
        return record[0]

    except (Exception, psycopg2.Error) as error:
        print("1) Error: ", error)

    finally:
        connection.commit()
        cursor_.close()


def insert_city(list_, connection):
    city_id = check_city_exists(list_['id'], connection)
    if city_id != -1:
        return city_id
    try:
        cursor = connection.cursor()

        postgres_insert_query = """ INSERT INTO city(api_city_id, name) VALUES (%s,%s) returning id"""
        record_to_insert = (list_['id'], list_['name'])
        cursor.execute(postgres_insert_query, record_to_insert)
        city_id = cursor.fetchone()[0]
        connection.commit()

    except (Exception, psycopg2.Error) as error:
        print("2) Error: ", error)

    finally:
        cursor.close()
        return city_id


def insert_metrics(list_, weather_id, connection):
    try:
        cursor = connection.cursor()
        postgres_insert_query = """ INSERT INTO metrics (temp, temp_max, temp_min, feels_like, humidity, 
        pressure, weather_id) VALUES (%s,%s,%s,%s,%s,%s,%s)"""
        record_to_insert = (list_['temp'], list_['temp_max'], list_['temp_min'], list_['feels_like'], list_['humidity'],
                            list_['pressure'], weather_id)
        cursor.execute(postgres_insert_query, record_to_insert)
        connection.commit()
    except (Exception, psycopg2.Error) as error:
        print("3) Error: ", error)

    finally:
        cursor.close()


def insert_wind(list_, weather_id, connection):
    try:
        cursor = connection.cursor()
        postgres_insert_query = """ INSERT INTO wind (speed, deg, weather_id) VALUES (%s,%s,%s)"""
        record_to_insert = (list_['speed'], list_['deg'], weather_id)
        cursor.execute(postgres_insert_query, record_to_insert)
        connection.commit()
    except (Exception, psycopg2.Error) as error:
        print("4) Error: ", error)

    finally:
        cursor.close()


def insert_clouds(list_, weather_id, connection):
    try:
        cursor = connection.cursor()
        postgres_insert_query = """ INSERT INTO clouds (cloudiness, weather_id) VALUES (%s,%s)"""
        record_to_insert = (list_['all'], weather_id)
        cursor.execute(postgres_insert_query, record_to_insert)
        connection.commit()
    except (Exception, psycopg2.Error) as error:
        print("5) Error: ", error)

    finally:
        cursor.close()


def insert_rain(list_, weather_id, connection):
    try:
        cursor = connection.cursor()
        postgres_insert_query = """ INSERT INTO rain (volume_hour, weather_id) VALUES (%s,%s)"""
        record_to_insert = (list_['1h'], weather_id)
        cursor.execute(postgres_insert_query, record_to_insert)
        connection.commit()
    except (Exception, psycopg2.Error) as error:
        print("6) Error: ", error)

    finally:
        cursor.close()


def insert_snow(list_, weather_id, connection):
    try:
        cursor = connection.cursor()
        postgres_insert_query = """ INSERT INTO snow (volume_hour, weather_id) VALUES (%s,%s)"""
        record_to_insert = (list_['1h'], weather_id)
        cursor.execute(postgres_insert_query, record_to_insert)
        connection.commit()
    except (Exception, psycopg2.Error) as error:
        print("7) Error: ", error)

    finally:
        cursor.close()


def insert_weather_data(list_, connection):
    try:
        city_id = insert_city(list_, connection)
        cursor = connection.cursor()

        postgres_insert_query = """ INSERT INTO weather (description, timestap, city_id) VALUES (%s,%s,%s) 
        returning id"""
        date = get_date(list_['dt'], list_['timezone'])
        record_to_insert = (list_['weather'][0]['main'], date.strftime('%Y-%m-%d %H:%M:%S'), city_id)
        cursor.execute(postgres_insert_query, record_to_insert)
        weather_id = cursor.fetchone()[0]
        connection.commit()

        if 'main' in list_:
            insert_metrics(list_['main'], weather_id, connection)

        if 'wind' in list_:
            insert_wind(list_['wind'], weather_id, connection)

        if 'clouds' in list_:
            insert_clouds(list_['clouds'], weather_id, connection)

        if 'rain' in list_:
            insert_rain(list_['rain'], weather_id, connection)

        if 'snow' in list_:
            insert_snow(list_['snow'], weather_id, connection)

    except (Exception, psycopg2.Error) as error:
        print("8) Error: ", error)

    finally:
        cursor.close()
