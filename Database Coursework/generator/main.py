import requests
from geopy.geocoders import Nominatim
from generator.weather_functions import *
from generator.forecast_functions import *
from generator.air_pollution_functions import *

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


def check_city_found(response_list):
    if 'cod' in response_list:
        if response_list['cod'] == '404':
            return False
        return True
    return True


def get_city_list_from_name(name, country):
    with open('cities/city_list/city.list.json', 'r', encoding='utf-8') as f:
        cities = json.load(f)

    for city_ in cities:
        if city_['name'] == name and city_['country'] == country:
            return city_


def get_current_weather_response_json(city_):
    url = CURRENT_WEATHER_URL.format(city_, API_KEY)
    res = requests.get(url)
    # print(json.dumps(res.json(), indent=4, sort_keys=True))
    return res.json()


def get_forecast_response_json(city_):
    url = FORECAST_URL.format(city_, API_KEY)
    res = requests.get(url)
    return res.json()


def get_air_pollution_response_json(name, country_ab):
    location = get_city_list_from_name(name, country_ab)
    global POLLUTION_CITY_ID
    POLLUTION_CITY_ID = location['id']
    url = AIR_POLLUTION_URL.format(location['coord']['lat'], location['coord']['lon'], API_KEY)
    res = requests.get(url)
    return res.json()


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
            insert_weather_data(weather_list, connection)
        elif int(options) == 2:
            forecast_list = get_forecast_response_json(city)
            found = check_city_found(forecast_list)
            if found is False:
                print('Error: ' + forecast_list['message'])
                break
            insert_forecast_data(forecast_list, connection)
        elif int(options) == 3:
            country = input('Enter country ab: ')
            pollution_list = get_air_pollution_response_json(city, country)
            if pollution_list == -1:
                print('Error: can`t find city inputted')
                break
            found = check_city_found(pollution_list)
            if found is False:
                print('Error: ' + pollution_list['message'])
                break
            if pollution_list is None:
                print('Error: city not found, check country and city')
                break
            pollution_list['id'] = POLLUTION_CITY_ID
            insert_air_pollution_data(pollution_list, connection)
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
