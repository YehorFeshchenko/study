from datetime import datetime
from colorama import Fore
import sys


def show_aqi(aqi):
    if aqi == 1:
        print("Air Quality is good")
    if aqi == 2:
        print("Air Quality is fair")
    if aqi == 3:
        print("Air Quality is moderate")
    if aqi == 4:
        print("Air Quality is poor")
    if aqi == 5:
        print("Air Quality is very poor")


class View:
    @staticmethod
    def print_header():
        print(Fore.CYAN + '\n-------------Weather analyzer-----------')
        print(Fore.LIGHTCYAN_EX + '1) Get weather by date from city chosen (+-4h)\n'
                                  '2) Get forecast by date (+-4h) from city chosen\n'
                                  '3) Get air pollution statistics by date from city chosen\n'
                                  '4) Show cities with highest temperature for current date\n'
                                  '5) Show cities with highest wind speed for current date\n'
                                  '6) Show cities with highest cloudiness for current date\n'
                                  '7) Show forecasts with highest probability of precipitation during current date\n'
                                  '8) Show cities that contain highest NO2 component for current date\n'
                                  '0) Quit')
        print(Fore.LIGHTMAGENTA_EX + 'Input number of function' + Fore.RESET)
        result = input()
        return result

    @staticmethod
    def get_city():
        city = input('Choose city: ')
        return city

    @staticmethod
    def get_datetime():
        date = input('Input date(YYYY-mm-dd HH:mm:ss): ')
        date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
        return date

    @staticmethod
    def get_date():
        date = input('Input date (YYYY-mm-dd): ')
        date = date + ' 00:00:00'
        date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
        return date

    @staticmethod
    def __check_input(user_input):
        return user_input.isdigit()

    @staticmethod
    def find_option():
        option = View.print_header()
        if option == '0':
            print('\nExit done')
            return 0
        if View.__check_input(option):
            if option == '1':
                return 1
            if option == '2':
                return 2
            if option == '3':
                return 3
            if option == '4':
                return 4
            if option == '5':
                return 5
            if option == '6':
                return 6
            if option == '7':
                return 7
            if option == '8':
                return 8
            print('Incorrect option, try again')
            return -1
        else:
            print('Incorrect input, check format')
            return -1

    @staticmethod
    def show_weather_metrics(desc, temp, feels_like, humidity, wind_speed, rain_volume, snow_volume, cloudiness):
        print(Fore.CYAN + '\nHere is your weather: ' + Fore.YELLOW)
        print("Description: " + desc)
        print("Temperature (Celsius): " + str(temp))
        print("Temperature feels like: " + str(feels_like))
        print("Humidity (%): " + str(humidity))
        print("Wind speed (m/s): " + str(wind_speed))
        if rain_volume is not None:
            print("Rain (volume for 1h): " + str(rain_volume))
        else:
            print("No rain")
        if snow_volume is not None:
            print("Snow (volume for 1h): " + str(snow_volume))
        else:
            print("No snow")
        if cloudiness is not None:
            print("Cloudiness (%): " + str(cloudiness))
        else:
            print("No clouds" + Fore.RESET)

    @staticmethod
    def show_forecast(desc, temp_max, temp_min, wind_speed, pop, cloudiness):
        print(Fore.CYAN + '\nHere is your forecast: ' + Fore.YELLOW)
        print("Description: " + desc)
        print("Max temperature (Kelvin): " + str(temp_max))
        print("Min temperature (Kelvin): " + str(temp_min))
        print("Probability of precipitation (*100%): " + str(pop))
        print("Wind speed (m/s): " + str(wind_speed))
        if cloudiness is not None:
            print("Cloudiness (%): " + str(cloudiness))
        else:
            print("No clouds" + Fore.RESET)

    @staticmethod
    def show_ap(aqi, comp_CO, comp_NO, comp_NO2):
        print(Fore.CYAN + '\nHere is your air pollution data: ' + Fore.YELLOW)
        show_aqi(aqi)
        print("CO component: " + str(comp_CO))
        print("NO component: " + str(comp_NO))
        print("NO2 component: " + str(comp_NO2))
