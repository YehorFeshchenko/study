from ..view.views import View
from .controller_functions import *
import time


def wait():
    time.sleep(int(1))


def menu():
    in_menu = True
    while in_menu:
        option = View.find_option()
        if option == 0:
            in_menu = False
            continue
        if option == -1:
            wait()
            continue
        if option == 1:
            city_temp = View.get_city()
            date_chosen = View.get_datetime()
            weather_list = get_weather_list_by_date(city_temp, date_chosen)
            if 'error' in weather_list:
                print("Error: " + weather_list['error'])
            else:
                View.show_weather_metrics(weather_list['desc'], weather_list['temp'], weather_list['feels_like'],
                                          weather_list['humidity'], weather_list['wind_speed'], weather_list['rain'],
                                          weather_list['snow'], weather_list['cloudiness'])
            continue
        if option == 2:
            city_temp = View.get_city()
            date_chosen = View.get_datetime()
            forecast_list = get_forecast_list_by_date(date_chosen, city_temp)
            if 'error' in forecast_list:
                print("Error: " + forecast_list['error'])
            else:
                View.show_forecast(forecast_list['desc'], forecast_list['temp_max'], forecast_list['temp_min'],
                                   forecast_list['wind_speed'], forecast_list['pop'], forecast_list['cloudiness'])
            continue
        if option == 3:
            city_temp = View.get_city()
            date_c = View.get_date()
            ap_list = get_ap_by_date(date_c, city_temp)
            if 'error' in ap_list:
                print("Error: " + ap_list['error'])
            else:
                View.show_ap(ap_list['aqi'], ap_list['comp_CO'], ap_list['comp_NO'], ap_list['comp_NO2'])
            continue
        if option == 4:
            date_ = View.get_date()
            error = get_hottest_cities(date_)
            if error is not None:
                print("Error: " + error)
            continue
        if option == 5:
            date_ = View.get_date()
            error = get_highest_wind_cities(date_)
            if error is not None:
                print("Error: " + error)
            continue
        if option == 6:
            date_ = View.get_date()
            error = get_highest_cloud_cities(date_)
            if error is not None:
                print("Error: " + error)
            continue
        if option == 7:
            date_ = View.get_date()
            error = get_cities_highest_pop(date_)
            if error is not None:
                print("Error: " + error)
            continue
        if option == 8:
            date_ = View.get_date()
            error = get_cities_highest_air_pollution(date_)
            if error is not None:
                print("Error: " + error)
            continue
        else:
            print('Incorrect option')
            continue
