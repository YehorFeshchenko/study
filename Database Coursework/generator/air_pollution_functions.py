import psycopg2
import json
import datetime
from generator.weather_functions import insert_city


def get_city_list_from_id(id_):
    with open('cities/city_list/city.list.json', 'r', encoding='utf-8') as f:
        cities = json.load(f)

    for city in cities:
        if city['id'] == id_:
            return city


def insert_air_pollution_data(list_, connection):
    try:
        city_list = get_city_list_from_id(list_['id'])
        city_id = insert_city(city_list, connection)

        cursor = connection.cursor()
        postgres_insert_query = """ INSERT INTO air_pollution (aqi, timestap, "comp_CO", "comp_NO", "comp_NO2", city_id) 
        VALUES (%s,%s,%s,%s,%s,%s)"""
        date = datetime.datetime.fromtimestamp(list_['list'][0]['dt'])
        components = list_['list'][0]['components']
        record_to_insert = (list_['list'][0]['main']['aqi'], date, components['co'], components['no'],
                            components['no2'], city_id)
        cursor.execute(postgres_insert_query, record_to_insert)
        connection.commit()

    except (Exception, psycopg2.Error) as error:
        print("10) Error: ", error)

    finally:
        cursor.close()