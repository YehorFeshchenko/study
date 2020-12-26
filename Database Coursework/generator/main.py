import requests
from geopy.geocoders import Nominatim
import psycopg2
import json
import datetime
from pytz import *
import calendar

API_KEY = '99774e5f095f2186a4cdc10a51221e47'
CURRENT_WEATHER_URL = 'http://api.openweathermap.org/data/2.5/weather?q={}&appid={}&units=metric'
AIR_POLLUTION_URL = 'http://api.openweathermap.org/data/2.5/air_pollution?lat={}&lon={}&appid={}'
FORECAST_URL = 'http://api.openweathermap.org/data/2.5/forecast?q={}&appid={}&cnt=5'


def get_password():
    f = open(r"D:\Job\Apps\password.txt", "r")
    data = f.read()
    f.close()
    return data


PASSWORD = get_password()

connection = psycopg2.connect(user="postgres", password=PASSWORD, host="localhost", database="Coursework")


def get_date(dt, tz):
    date = dt + tz
    return datetime.datetime.fromtimestamp(date)


def check_city_found(response_list):
    if response_list['cod'] == '404':
        return False
    return True


def get_current_weather_response_json(city_):
    url = CURRENT_WEATHER_URL.format(city_, API_KEY)
    res = requests.get(url)
    # print(json.dumps(res.json(), indent=4, sort_keys=True))
    return res.json()


def get_forecast_response_json(city_):
    url = FORECAST_URL.format(city_, API_KEY)
    res = requests.get(url)
    return res.json()


def get_air_pollution_response_json(city_):
    geolocator = Nominatim(user_agent="courseworkGeolocator")
    location = geolocator.geocode(city_)
    # print("lat = ")
    # print(location.lattitude)
    # print("lon = ")
    # print(location.longitude)
    url = AIR_POLLUTION_URL.format(location.lattitude, location.longitude, API_KEY)
    res = requests.get(url)
    return res.json()


def check_city_exists(id_):
    try:
        cursor_ = connection.cursor()

        postgres_insert_query = """ SELECT * from city where api_city_id = %s"""
        record_to_insert = (id_,)
        cursor_.execute(postgres_insert_query, record_to_insert)
        record = cursor_.fetchone()
        if record is None:
            return -1
        return record[0]
        connection.commit()

    except (Exception, psycopg2.Error) as error:
        print("1) Error: ", error)

    finally:
        cursor_.close()


def insert_city(list_):
    city_id = check_city_exists(list_['id'])
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


def insert_metrics(list_, weather_id):
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


def insert_wind(list_, weather_id):
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


def insert_clouds(list_, weather_id):
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


def insert_rain(list_, weather_id):
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


def insert_snow(list_, weather_id):
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


def insert_weather_data(list_):
    try:
        city_id = insert_city(list_)
        cursor = connection.cursor()

        postgres_insert_query = """ INSERT INTO weather (description, timestap, city_id) VALUES (%s,%s,%s) 
        returning id"""
        date = get_date(list_['dt'], list_['timezone'])
        record_to_insert = (list_['weather'][0]['main'], date.strftime('%Y-%m-%d %H:%M:%S'), city_id)
        cursor.execute(postgres_insert_query, record_to_insert)
        weather_id = cursor.fetchone()[0]
        connection.commit()

        if 'main' in list_:
            insert_metrics(list_['main'], weather_id)

        if 'wind' in list_:
            insert_wind(list_['wind'], weather_id)

        if 'clouds' in list_:
            insert_clouds(list_['clouds'], weather_id)

        if 'rain' in list_:
            insert_rain(list_['rain'], weather_id)

        if 'snow' in list_:
            insert_snow(list_['snow'], weather_id)

    except (Exception, psycopg2.Error) as error:
        print("8) Error: ", error)

    finally:
        cursor.close()


while True:
    city = input('Choose the city to get data about: ')
    print('Choose what type of weather data you want to get:')
    print('1) Current weather\n2) Weather forecast\n3) Air pollution')
    options = input()
    if options.isdigit():
        if int(options) == 1:
            weather_list = get_current_weather_response_json(city)
            found = check_city_found(weather_list)
            if found is False:
                print('Error: ' + weather_list['message'])
                break
            insert_weather_data(weather_list)
            # print(weather_list['name'])
        elif int(options) == 2:
            forecast_list = get_forecast_response_json(city)
            found = check_city_found(forecast_list)
            if found is False:
                print('Error: ' + forecast_list['message'])
                break
            # print(forecast_list['city']['name'])
        elif int(options) == 3:
            pollution_list = get_air_pollution_response_json(city)
            found = check_city_found(pollution_list)
            if found is False:
                print('Error: ' + pollution_list['message'])
                break
            # print(pollution_list['name'])
        else:
            print('Incorrect choice')
            continue
        print('Data generated')
        break
    else:
        print('Incorrect choice')
        continue

if connection:
    connection.close()
