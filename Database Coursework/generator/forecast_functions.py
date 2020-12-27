import psycopg2
import datetime
from generator.weather_functions import insert_city


def insert_indicators(list_, connection, forecast_id):
    try:
        cursor = connection.cursor()
        postgres_insert_query = """ INSERT INTO indicators (temp_max, temp_min, cloudiness, 
        pop, wind_speed, forecast_id) VALUES (%s,%s,%s,%s,%s,%s)"""
        record_to_insert = (list_['main']['temp_max'], list_['main']['temp_min'], list_['clouds']['all'],
                            list_['pop'], list_['wind']['speed'], forecast_id)
        cursor.execute(postgres_insert_query, record_to_insert)
        connection.commit()
    except (Exception, psycopg2.Error) as error:
        print("Error: ", error)

    finally:
        cursor.close()


def insert_forecast_data(list_, connection):
    try:
        city_id = insert_city(list_['city'], connection)

        for forecast in list_['list']:
            cursor = connection.cursor()
            postgres_insert_query = """ INSERT INTO forecast (description, timestap, city_id) VALUES (%s,%s,%s) 
                    returning id"""
            record_to_insert = (forecast['weather'][0]['description'], forecast['dt_txt'], city_id)
            cursor.execute(postgres_insert_query, record_to_insert)
            forecast_id = cursor.fetchone()[0]
            connection.commit()

            insert_indicators(forecast, connection, forecast_id)

    except (Exception, psycopg2.Error) as error:
        print("9) Error: ", error)

    finally:
        cursor.close()
